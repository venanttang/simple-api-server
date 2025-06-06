
import logging
from queue import Queue
import queue
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from contextlib import asynccontextmanager
from tests.json_helper import lookup_json_by_id
from tree_item_response import TreeItemResponse
from sqlalchemy import text



# ---------------------
# Configure Logging
# ---------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
debug:bool = False
if debug:
    logger.setLevel(logging.DEBUG)
logger.info(f"debug={debug}")

# ---------------------
# Database Model
# ---------------------
class TreeItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    label: str
    parentId: Optional[int] = Field(default=None, foreign_key="treeitem.id", index=True)


# ---------------------
# Setup FastAPI & DB
# ---------------------

# Set the SQLite database file name
sqlite_file = "database.db"
# TODO: change to memory mode later...
# ...

# Create the SQLite database engine
engine = create_engine(f"sqlite:///{sqlite_file}", 
                       echo=debug, 
                       pool_pre_ping=True,
                       connect_args={
                           "check_same_thread": False,
                           "timeout": 30,
                           }
                       )

# TODO: create backup instance of the database...
# ...

# Execute a PRAGMA to enable WAL mode for SQLite to improve concurrency
def enable_wal():
    try:
        with engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL;"))
    except Exception as e:
        logger.error(f"Failed to enable WAL mode: {e.__class__.__name__}: {e}")

enable_wal()
        
# ------------------------
# Create the table
# ------------------------
@asynccontextmanager
async def lifespan_context(app: FastAPI):
    logger.info("Starting up the SimpleAPIServer application...")
    SQLModel.metadata.create_all(engine)
    # TODO: load the backup instance of the database to memory (primary instance)
    # ...
    
    yield
    logger.info("Shutting down the SimpleAPIServer application...")
    # TODO: Copy & wrap up all the changes to the backup instance of the database from primary instance
    # ...
    
    # Cleanup code can be added here if needed
    # Close the database connection if needed
    # engine.dispose()

app = FastAPI(lifespan=lifespan_context)


def get_session():
    logger.info("Creating a new database session...")
    with Session(engine) as session:
        yield session
        logger.info("Closing the database session...")
        

write_queue:Queue = Queue(maxsize=1000)  # 0 means infinite size

def queue_up_for_write(item: TreeItem):
    logger.info(f"Queueing up item for write: {item}")
    try:
        if item is not None and write_queue is not None:
            write_queue.put_nowait(item)
            logger.info(f"Item queued successfully: {item}")
        return item
    except queue.Full:
        logger.error(f"Queue is full, item not added: {item}")
    except Exception as e:
        logger.error(f"Error queueing item: {item}, Error: {e}")
    return None

def process_write_queue():
    logger.info("Starting up write queue...")
    while True:
        try:
            if write_queue is not None:
                item:TreeItem = write_queue.get()
                logger.info(f"Processing item: {item}")
                if item is not None:
                    write_to_db(item)
        except Exception as e:
            logger.error(f"Error processing item: {item}, Error: {e.__class__.__name__}: {e}")
        finally:
            # Mark the task as done
            # This is important to avoid blocking the queue
            if write_queue is not None:
                write_queue.task_done()
    return
        
# Start the write queue processing in a separate thread
import threading
write_thread = threading.Thread(target=process_write_queue, daemon=True)
logger.info("Starting write queue processing thread...")
write_thread.start()

def write_to_db(item: TreeItem) -> TreeItem:
    if item is not None:
        logger.info(f"Writing item to DB: {item}")
        with Session(engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
    return item

# ---------------------
# POST: Create Item
# ---------------------
@app.post("/api/tree", response_model=TreeItem)
async def create_item(item: TreeItem):
    queue_up_for_write(item)
    return item


# ---------------------
# GET: List Raw Items (debugging only)
# ---------------------
# TODO: remove this endpoint later...
# @app.get("/api/raw", response_model=List[TreeItem])
# async def read_raw_items(session: Session = Depends(get_session)):
#     logger.info("Received request to list items.")
#     items = session.exec(select(TreeItem)).all()
#     logger.info(f"Items found: {items}")
#     return items

# ---------------------
# GET: List Items
# ---------------------
# @app.get("/api/tree", response_model=List[Item])
@app.get("/api/tree", response_model=List[TreeItemResponse])
async def read_items(session: Session = Depends(get_session)):
    logger.info("Received request to list TreeItemResponses.")
    response:List[TreeItemResponse] = []
    rootItemResponse:TreeItemResponse = None
    # Get the root item (the one with no parent)
    rootItem:TreeItem = session.exec(select(TreeItem).where(TreeItem.parentId == None)).first()
    if rootItem is not None:
        rootItemResponse = get_ItemResponse(rootItem, session)
        response.append(rootItemResponse)
    else:
        logger.info(f"Root item NOT found")

    return response

def get_ItemResponse(item: TreeItem, session: Session) -> TreeItemResponse:
    return TreeItemResponse(id=item.id, label=item.label, children=get_ItemResponseChildren(item, session))

def get_ItemResponseChildren(item: TreeItem, session: Session) -> List[TreeItemResponse]:
    children = []

    # fetch all children of the item
    logger.debug(f"Fetching children for item ID: {item.id}")
    for child in session.exec(select(TreeItem).where(TreeItem.parentId == item.id)).all():
        logger.debug(f"Child item found: {child}")
        # Recursively get the children of the child item
        children.append(get_ItemResponse(child, session))
    
    return children

def get_item_by_id(itemId:int, session: Session) -> TreeItem:
    item:TreeItem = session.exec(select(TreeItem).where(TreeItem.id == itemId)).first()
    if item is None:
        logger.info(f"Item with ID {itemId} NOT found")
        return None
    logger.info(f"Item with ID {itemId} found: {item}")
    return item


# @app.get("/api/tree", response_model=List[Item])
@app.post("/api/clone")
async def clone_items(idNodeToBeCloned:int, destinationId:int, session: Session = Depends(get_session)):
    logger.info(f"Received request to clone item with ID {idNodeToBeCloned} to destination ID {destinationId}.")
    itemToBeCloned:TreeItem = session.exec(select(TreeItem).where(TreeItem.id == idNodeToBeCloned)).first()
    if itemToBeCloned is None:
        logger.info(f"Item to be cloned NOT found")
        return []

    # Get the item to be cloned
    logger.info(f"Item to be cloned found: {itemToBeCloned}")        
    clone_children_recursively(itemToBeCloned, destinationId, session)
    return

def clone_children_recursively(itemToBeCloned:TreeItem, destinationParentId:int, session: Session):
    logger.info(f"Cloning children of item {itemToBeCloned} to destination parent ID {destinationParentId}.")
    
    # Get the children of the item to be cloned
    children:List[TreeItem] = session.exec(select(TreeItem).where(TreeItem.parentId == itemToBeCloned.id)).all()
    if children is None:
        logger.info(f"Children of the item to be cloned NOT found")
        return []
    if len(children) == 0:
        logger.info(f"Children of the item to be cloned NOT found")
        return []
    
    logger.info(f"Children of the item to be cloned found: {children}")
    
    # Clone the children items
    for child in children:
        logger.info(f"Cloning child item: {child}")
        clonedChild:TreeItem = TreeItem(label=child.label, parentId=destinationParentId)
        try:
            logger.info(f"Setting the cloned child item {clonedChild} under {destinationParentId}")
            write_to_db(clonedChild)

            # Recursively clone the children of the child
            clone_children_recursively(child, clonedChild.id, session)
        except Exception as e:
            logger.error(f"Error writing cloned child item to DB: {e.__class__.__name__}: {e}")
            return []
        
    logger.info(f"Finished cloning children of item {itemToBeCloned} to destination parent ID {destinationParentId}.")
    return
