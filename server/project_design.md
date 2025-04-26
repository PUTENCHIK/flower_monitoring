# Flowers Monitoring

## API Endpoints

### Registration

POST `/devices/register`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
    "config": {
        "name": "Дача",
        "ports": [
            "port1": {
                "enabled": true,
                "name": "Кактус Дэни",
                "low_level_boundary": 300,
                "medium_level_boundary": 470,
            },
            "port2": {
                "enabled": false,
                "name": "Кактус Мэкси",
                "low_level_boundary": 300,
                "medium_level_boundary": 470,
            }
        ],
    }
}
```

### Update data

PATCH `/devices/data`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
    "data": [
        "port1": {
            "value": 215
        },
        "port2": {
            "value": 400,
        }
    ]
}
```

### Getting data

GET `/devices/data`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul"
}
```

+ Response
```
{
    "name": "Дача",
    "last_activity": "25.04.2025 11:03",
    "data": [
        "port1": {
            "name": "Кактус Дэни",
            "value": 13,
            "state": "low"
        },
        "port2": {
            "name": "Кактус Мэкси",
            "value": 57,
            "status": "medium"
        }
    ]
}
```

### Update config

PATCH `/devices/config`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
    "config": {
        "name": "Дача",
        "ports": [
            "port1": {
                "enabled": true,
                "name": "Кактус Дэни",
                "low_level_boundary": 300,
                "medium_level_boundary": 470,
            },
            "port2": {
                "enabled": false,
                "name": "Кактус Мэкси",
                "low_level_boundary": 300,
                "medium_level_boundary": 470,
            }
        ],
    }
}
```


## Database design

`devices.db`

```
devices (   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deviceToken TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    last_activity DateTime,
    created_at DateTime NOT NULL,
    deleted_at DateTime
)
```

```
ports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    sensor_value INTEGER,
    port_number INTEGER NOT NULL,
    enabled BOOLEAN NOT NULL,
    name TEXT NOT NULL,
    low_level_boundary INTEGER,
    medium_level_boundary INTEGER,
    FOREIGN KEY (device_id) REFERENCES devices(id)
)
```