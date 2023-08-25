data = {
                "parent": {"type": "database_id", "database_id": "49f70ebd825a4c85a2a13b9ea10180b8"},
                'properties': {
                    "relation": {
                        "relation": [
                            {
                                "id": "6c214fd7f70348728b21089c2318e243",
                            },
                            {
                                "id": "cfd93e8b93c44a73b08f474cb66e491e",
                            }
                        ]

                    },
                }
            }

new_id = "new_id_value"  # 你要添加的新ID的值
data['properties']['relation']['relation'].append({"id": new_id})
data['properties']['relation']['relation'].append({"id": "cfd93e8b93c44a73b08f474cb66e491e",})
print(data)