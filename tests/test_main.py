import logging
from fastapi.testclient import TestClient
from httpx import Response
from main import TreeItem
from tests.json_helper import lookup_id_by_label, remove_id, validate_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

target_host = "http://localhost:8000"
target_url = f"{target_host}/api/tree"
target_raw_url = f"{target_host}/api/raw"

json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "label": {
                "type": "string"
            },
            "children": {
                "type": "array",
                "items": {
                    "$ref": "#/items"  # Recursive reference to the same structure
                }
            }
        },
        "required": ["label", "children"]
    }
}

# Define the expected JSON structure
target_json = [
    {
        "id": 1,
        "label": "root",
        "children": [
            {
                "id": 3,
                "label": "bear",
                "children": [
                    {
                        "id": 4,
                        "label": "cat",
                        "children": [
                            {
                                "id": 8,
                                "label": "cat_child",
                                "children": []
                            }
                        ]
                    },
                ]
            },
            {
                "id": 7,
                "label": "frog",
                "children": []
            }
        ]
    }
]

def getIdByLabel(client:TestClient, label:str) -> int:
    if client is None:
        logger.warning("client is None")
        return -1
    
    response:Response = client.get(target_url)
    return lookup_id_by_label(response.json(), label)

def test_create_and_read_tree(client: TestClient) -> None:
    # Create the tree structure
    # with ThreadPoolExecutor() as executor:
    #     rootId:int = 1
    #     bearId:int = 3
    #     frogId:int = 7
    #     catId:int = 4

    #     futures = [
    #         # Create the root item
    #         executor.submit(add_item, client, "root", None),
    #         # # Create the bear item
    #         executor.submit(add_item, client, "bear", rootId, 3),
    #         # # Create the frog item
    #         executor.submit(add_item, client, "frog", rootId, 7),
    #         # # Create the cat item
    #         executor.submit(add_item, client, "cat", bearId, 4),
    #         # # Create the cat_child item
    #         executor.submit(add_item, client, "cat_child", catId),
    #     ]
        
    #     # Wait for all futures to complete
    #     # results = [future.result() for future in as_completed(futures)]
    #     for future in futures:
    #         logger.info(f'Future result: {future.result()}')

    # Create the root item
    add_item(client, "root", None)
    rootId:int = getIdByLabel(client, "root")
    
    add_item(client, "bear", rootId, 3)
    bearId:int = getIdByLabel(client, "bear")
    
    add_item(client, "frog", rootId, 7)
    frogId:int = getIdByLabel(client, "frog")
    
    add_item(client, "cat", bearId, 4)
    catId:int = getIdByLabel(client, "cat")
    
    add_item(client, "cat_child", catId, 8)
    cat_childId:int = getIdByLabel(client, "cat_child")    


    raw_response:Response = client.get(target_raw_url)
    assert raw_response.status_code == 200
    raw_items = raw_response.json()
    logger.info(f"raw_items: {raw_items}")

    # Test retrieving the tree structure
    response:Response = client.get(target_url)
    assert response.status_code == 200
    tree = response.json()
    logger.info(f"tree: {tree}")
    
    # Validate the response against the schema
    validate_json(tree, json_schema)
    
    root_1 = remove_id(tree)
    root_2 = remove_id(target_json)
    logger.info(f"root_1: {root_1}")
    logger.info(f"root_2: {root_2}")
    logger.info(f"root_1 == root_2: {root_1 == root_2}")
    assert root_1 == root_2
    return

def add_item(client: TestClient, label:str, parentId:int, id:int = -1) -> TreeItem:
    if client is None:
        logger.warning("client is None")
        return None
    if label is None:
        logger.warning("label is None")
        return None
    
    myJson = {
        # "id": id,
        "label": label,
        "parentId": parentId
    }
    if id != -1:
        myJson["id"] = id
    
    response:Response = client.post(target_url, json=myJson)
    assert response.status_code == 200
    
    logger.info(f"here myJson Request: {myJson} --- Response: {response.json()}")
    
    myTestItem:TreeItem = TreeItem.model_validate(response.json())
    assert myTestItem.label == label
    # assert myTestItem.id is not None
    if parentId is None:
        assert myTestItem.parentId is None
    else:
        assert myTestItem.parentId == parentId
    return myTestItem.id