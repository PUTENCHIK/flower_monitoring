<template>
    <div class="main-page">
        <div class="content ">
            <form @submit="addDevice" class="form-add-device">
                <span :class="messageClass" >{{ messageValue }}</span>
                <input minlength="4" maxlength="40" @change="addDeviceInputChange" :class="addDeviceInputClass" v-model="addDeviceInputValue" type="search" name="" id="" placeholder="Токен устройства...">
                <button class="form-add-device__submit" type="submit">Добавить</button>
            </form>
        </div>
        <div class="devices">
            <DeviceSection v-for="(item) in devices"
                :key="item.deviceToken"
                :device="item"
                @device-deleted="handleDeviceDeleted"/>
        </div>

    </div>

</template>

<script setup>
    import DeviceSection from './DeviceSection.vue';
    import axios from 'axios';
    import { ref, onMounted, reactive  } from 'vue';

    const addDeviceInputValue = ref("");
    const addDeviceInputClass = ref({
        "form-add-device__input": true,
        "form-add-device__input--success": false,
        "form-add-device__input--failed": false,
    })

    const messageValue = ref("");
    const messageClass = ref({
        "message": true,
        "message--success": false,
        "message--failed": false,
    });

    const devices = reactive([]);


    async function addDevice(event) {
        event.preventDefault();

        if (addDeviceInputValue.value.trim() < 5) {
            messageValue.value = "Длина токена устройства должна быть не менее 4 символов!";
            messageClass.value = {
                "message": true,
                "message--success": false,
                "message--failed": true,
            };
            addDeviceInputClass.value = {
                "form-add-device__input": true,
                "form-add-device__input--success": false,
                "form-add-device__input--failed": true,
            };
            return;
        }

        try {
            const response = await axios.post('http://localhost:5050/devices/data', {
                deviceToken: addDeviceInputValue.value
            });
            console.log('Успешный ответ:', response.data);

            addDeviceInputClass.value = {
                "form-add-device__input": true,
                "form-add-device__input--success": true,
                "form-add-device__input--failed": false,
            };

            let checkTokens = localStorage.getItem("deviceTokens");
            let tokens = [];
            if (checkTokens !== null) {
                tokens = JSON.parse(checkTokens)
            }
            
            messageClass.value = {
                "message": true,
                "message--success": true,
                "message--failed": false,
            };
            if (tokens.includes(addDeviceInputValue.value)) {
                messageValue.value = "Это устройство уже добавлено!"
                return;
            }

            messageValue.value = "Успех!"
            tokens.push(addDeviceInputValue.value);
            localStorage.setItem("deviceTokens", JSON.stringify(tokens));

            pushDeviceToDevices(response.data, addDeviceInputValue.value)

        } catch (error) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 404:
                        console.log('Ресурс не найден:', error.response.data);
                        messageValue.value = "Устройство не найдено"
                        messageClass.value = {
                            "message": true,
                            "message--success": false,
                            "message--failed": true,
                        };
                        addDeviceInputClass.value = {
                            "form-add-device__input": true,
                            "form-add-device__input--success": false,
                            "form-add-device__input--failed": true,
                        };
                        break;
                    default:
                        console.log('Данные ошибки:', error.response.data);
                        console.log('Код состояния:', error.response.status);
                        console.log('Заголовки:', error.response.headers);
                }
            } else if (error.request) {
                console.log('Запрос:', error.request);
            } else {
                console.log('Ошибка:', error.message);
            }
        }
    }

    function addDeviceInputChange() {
        addDeviceInputClass.value = {
            "form-add-device__input": true,
            "form-add-device__input--success": false,
            "form-add-device__input--failed": false,
        };

        messageClass.value = {
            "message": true,
            "message--success": false,
            "message--failed": false,
        };

        messageValue.value = "";
    }

    function pushDeviceToDevices(data, deviceToken) {
        let backgroundColor = "#EBF5FB";
        if (devices.length % 2 == 0) {
            backgroundColor = "#fff";
        }

        let ports = {};
        for (let key in data.ports) {
            ports[key] = {
                "name": data.ports[key].name,
                "value": data.ports[key].value,
                "state": data.ports[key].state,
            };
        }

        let device = {
            name: `${data.name} (${deviceToken.slice(0, 7)}...)`,
            lastActivity: data.last_activity,
            backgroundColor: backgroundColor,
            deviceToken: deviceToken,
            ports: ports
        }

        devices.push(device);
    }

    async function getDevices() {
        let checkLocalDevices = localStorage.getItem("deviceTokens");
        let localDevices = [];

        if (checkLocalDevices !== null) {
            localDevices = JSON.parse(checkLocalDevices);
        }
        else {
            return;
        }

        localDevices.forEach(async deviceToken => {
            try {
                const response = await axios.post('http://localhost:5050/devices/data', {
                    deviceToken: deviceToken
                });
                console.log('Успешный ответ:', response.data);
                
                pushDeviceToDevices(response.data, deviceToken)

            } catch (error) {
                console.log('Ошибка при запросе:', error);

                if (error.response) {
                    switch (error.response.status) { 
                        case 404:
                            console.log('Ресурс не найден:', error.response.data);
                            break;
                        default:
                            console.log('Данные ошибки:', error.response.data);
                            console.log('Код состояния:', error.response.status);
                            console.log('Заголовки:', error.response.headers);
                    }
                } else if (error.request) {
                    console.log('Запрос:', error.request);
                } else {
                    console.log('Ошибка:', error.message);
                }
            }
            }); 
    }
    
    const handleDeviceDeleted = (deviceToken) => {
        let checkTokens = localStorage.getItem("deviceTokens");
        if (checkTokens === null) {
            return;
        }
        let tokens = JSON.parse(checkTokens);
        let index = tokens.indexOf(deviceToken);
        if (index !== -1) {
            tokens.splice(index, 1);
        }
        localStorage.setItem("deviceTokens", JSON.stringify(tokens));


        index = devices.findIndex(device => device.deviceToken === deviceToken);
        if (index !== -1) {
            devices.splice(index, 1);
        }
    };

    onMounted(async () => {
        await getDevices();
    });
    

</script>


<style scoped>
    .main-page {
        background-color: #EBF5FB;
    }

    .form-add-device__input {
        font-family: "Montserrat";
        width: 433px;
        height: 53px;
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 20px;
        border: 3px solid rgb(133, 128, 128);
        padding-left: 12px;
        padding-right: 12px;
        margin-right: 16px;
    }

    .form-add-device__submit {
        font-family: "Montserrat";
        background-color: #113259;
        color: #fff;
        width: 124px;
        height: 53px;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    .form-add-device__submit:hover {
        background-color: #0e2848;
    }

    .form-add-device {
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        padding: 24px 0px;
        align-items: center;
    }

    .form-add-device__input--success {
        border: "3px solid #86e363";
    }

    .form-add-device__input--failed {
        border: "3px solid #f04848";
    }

    .message {
        font-family: "Montserrat";
        font-size: 20px;
        margin-right: 16px;
        font-weight: 500;
    }

    .message--failed {
        color: #f04848;
    }

    .message--success {
        color: #86e363;
    }
</style>
