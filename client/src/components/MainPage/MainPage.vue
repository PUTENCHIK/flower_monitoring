<template>
    <div class="main-page">
        <div class="content ">
            <form @submit="addDevice" class="form-add-device">
                <span :class="messageClass" >{{ messageValue }}</span>
                <input @change="addDeviceInputChange" :class="addDeviceInputClass" v-model="addDeviceInputValue" type="search" name="" id="" placeholder="Токен устройства...">
                <button class="form-add-device__submit" type="submit">Добавить</button>
            </form>
        </div>
        <DeviceSection 
            name="Дача (dKde123...)"
            backgroundColor="#f2f3f4"
        />
    </div>

</template>

<script setup lang="ts">
    import DeviceSection from './DeviceSection.vue';
    import axios from 'axios';
    import { ref, onMounted } from 'vue';

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


    async function addDevice(event: Event) {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:5050/devices/data', {
                deviceToken: addDeviceInputValue.value
            });
            console.log('Успешный ответ:', response.data);

            messageValue.value = "Успех!"
            messageClass.value = {
                "message": true,
                "message--success": true,
                "message--failed": false,
            };
            addDeviceInputClass.value = {
                "form-add-device__input": true,
                "form-add-device__input--success": true,
                "form-add-device__input--failed": false,
            };

            let checkTokens = localStorage.getItem("deviceTokens");
            let tokens: string[] = [];
            if (checkTokens !== null) {
                tokens = JSON.parse(checkTokens)
            }
            
            tokens.push(addDeviceInputValue.value);
            localStorage.setItem("deviceTokens", JSON.stringify(tokens));

            return response.data;
        } catch (error: any) {
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

    function addDeviceInputChange(event: Event) {
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



    // const fetchData = async () => {
    //     try {
    //         const response = await axios.get('http://localhost:5050/');
    //         data.value = response.data;
    //     } catch (error) {
    //         console.error('Ошибка при получении данных:', error);
    //         // Обработайте ошибку
    //     }
    // };

    // onMounted(() => {
    //     fetchData();
    // });






</script>


<style scoped>
    .main-page {
        background-color: #f2f3f4;
    }

    .form-add-device__input {
        font-family: "Montserrat";
        width: 433px;
        height: 53px;
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 18px;
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
