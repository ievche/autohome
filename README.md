# Device Registry

### API

**`GET /devices`**

- `200 OK`

```json response
[
	{
		"identifier": "bedroom-heater",
  		"name": "Bedroom Heater",
		"device_type": "switch",
		"controller_gateway": "192.168.0.5
	}
]
```

**`POST /devices`**

```json body
{
 	"identifier": "bedroom-heater",
        "name": "Bedroom Heater",
        "device_type": "switch",
        "controller_gateway": "192.168.0.5
}
```

- `201 OK`

**`GET /device/<identifier>`**

- `200 OK`
- `404 Not Found`

**`DELETE /device/<identifier>`**

- `204 Not Content`
- `404 Not Found`
