pipeline = [
    {
        "$addFields": {
            "hour": { "$hour": "$created_at" }
        }
    },
    {
        "$match": {
            "hour": { "$gte": 6, "$lt": 24 }  
        }
    },
    {
        "$group": {
            "_id": {
                "period": {
                    "$switch": {
                        "branches": [
                            { 
                                "case": { 
                                    "$and": [
                                        { "$gte": ["$hour", 6] }, 
                                        { "$lt": ["$hour", 12] }
                                    ]
                                }, 
                                "then": "morning" 
                            },
                            { 
                                "case": { 
                                    "$and": [
                                        { "$gte": ["$hour", 12] }, 
                                        { "$lt": ["$hour", 18] }
                                    ]
                                }, 
                                "then": "afternoon" 
                            },
                            { 
                                "case": { 
                                    "$and": [
                                        { "$gte": ["$hour", 18] }, 
                                        { "$lt": ["$hour", 24] }
                                    ]
                                }, 
                                "then": "night" 
                            }
                        ],
                        "default": "unknown"
                    }
                }
            },
            "average_number": { "$avg": "$number" }
        }
    },
    {
        "$project": {
            "_id": 0,
            "period": "$_id.period",
            "average_number": 1
        }
    },
    {
        "$sort": { "period": 1 }  # 시간대 순으로 정렬
    }
]
