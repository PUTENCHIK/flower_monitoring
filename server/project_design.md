# Flowers Monitoring

## API Endpoints

### Registration

POST `/devices/register`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
}
```

### Update data

PATCH `/devices/data`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
    "ports": {
        "1": {
            "value": 215
        },
        "2": {
            "value": 400
        }
    }
}
```

### Getting data

POST `/devices/data`

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
    "ports": {
        "1": {
            "name": "Кактус Дэни",
            "value": 13,
            "state": "low"
        },
        "2": {
            "name": "Кактус Мэкси",
            "value": 57,
            "status": "medium"
        }
    }
}
```

### Check password

POST `/devices/password`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty"
}
```


### Get config

POST `/devices/config`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
}
```

+ Response
```
{
    "name": "Дача",
    "last_activity": "25.04.2025 11:03",
    "ports": {
        "1": {
            "enabled": true,
            "name": "Кактус Дэни",
            "low_level_boundary": 30,
            "medium_level_boundary": 60,
        },
        "2": {
            "enabled": false,
            "name": "Кактус Мэкси",
            "low_level_boundary": 20,
            "medium_level_boundary": 60,
        }
    }
}
```

### Update config

PUT `/devices/config`

+ Request
```
{
    "deviceToken": "dJdq4Rl9ul",
    "password": "qwerty",
    "new_password": "qwerty123"
    "config": {
        "name": "Дача",
        "ports": {
            "1": {
                "enabled": true,
                "name": "Кактус Дэни",
                "low_level_boundary": 30,
                "medium_level_boundary": 60,
            },
            "2": {
                "enabled": false,
                "name": "Кактус Мэкси",
                "low_level_boundary": 20,
                "medium_level_boundary": 60,
            }
        },
    }
}
```


## Database design

`devices.db`

```
devices (   
    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceToken = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    last_activity = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    ports = relationship("Port", back_populates="device")
    chat_ids = relationship("DeviceChatIDs", back_populates="device")
)
```

```
ports(
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    sensor_value = Column(Integer, nullable=True)
    port_number = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False)
    name = Column(String(255), nullable=False)
    low_level_boundary = Column(Integer, nullable=True)
    medium_level_boundary = Column(Integer, nullable=True)
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    device = relationship("Device", back_populates="ports")
)
```

```
device_chat_ids(
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    chat_id = Column(String(255), nullable=True)
    device = relationship("Device", back_populates="chat_ids")
)
```