<template>
    <div class="content">
        <div class="settings-wrapper">
            <h1>Настройка устройства</h1>
            <form @submit="changeConfig">
                <div class="config-block config-main">
                    <label>
                        Имя устройства:
                        <br>
                        <input maxlength="40" v-model="deviceNameModel" type="text" name="" placeholder="Введите имя устройства">
                    </label>
                    <label>
                        Сменить пароль: 
                        <br>
                        <input v-model="changePasswordModel" type="checkbox" name="" >
                    </label>
                    <div v-if="changePasswordModel" class="new-password-block">
                        <label>
                            Новый пароль: 
                            <br>
                            <input minlength="4" required v-model="newPasswordModel" type="password" name="" placeholder="Введите новый пароль устройства">
                        </label>
                        <label>
                            Повторно введите новый пароль: 
                            <br>
                            <input minlength="4" required v-model="newPasswordAgainModel" type="password" name="" placeholder="Введите новый пароль устройства">
                        </label>
                    </div>
                    <span v-if="messageValueMain" class="message"> {{ messageValueMain }}</span>
                </div>

                <fieldset v-for="(sensor, index) in sensors" :key="index" class="config-block">
                    <legend>Датчик {{ index }}</legend>
                    <label>
                        Имя датчика:
                        <br>
                        <input minlength="4" maxlength="40" v-model="sensor.name" type="text" placeholder="Введите имя датчика">
                    </label>
                    <label class="checkbox_label">
                        Отслеживать:
                        <input v-model="sensor.enabled" type="checkbox">
                    </label>
                    <label>
                        Критический порог (%):
                        <br>
                        <input min="1" max="100" v-model="sensor.low_level_boundary" type="number" placeholder="Введите критический порог">
                    </label>
                    <label>
                        Приемлемый порог (%):
                        <br>
                        <input min="1" max="100" v-model="sensor.medium_level_boundary" type="number" placeholder="Введите приемлемый порог">
                    </label>

                    <span v-if="messageValueSensors[index]" class="message"> {{ messageValueSensors[index] }}</span>
                </fieldset>

                <label>
                    Введите пароль для подтвердения:
                    <br>
                    <input required v-model="passwordModel" type="password" name="" placeholder="Введите пароль устройства">
                </label>

                <span v-if="messageValueLast" class="message"> {{ messageValueLast }}</span>
                <div class="settings-submit-button-wrapper">
                    <button class="settings-submit-button" type="submit">Отправить</button>
                </div>
  
            </form>
        </div>
    </div>
</template>

<script setup>
    import axios from 'axios';
    import { reactive, ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    

    const router = useRouter()

    const props = defineProps({
        deviceToken: {
            type: String,
            required: true,
        }
    });

    const deviceNameModel = ref("");
    const passwordModel = ref("");
    const newPasswordModel = ref("");
    const newPasswordAgainModel = ref("");
    const changePasswordModel = ref(false);

    const sensors = reactive({});
    const messageValueMain = ref("");
    const messageValueLast = ref("");
    const messageValueSensors = reactive([]);

    async function changeConfig(event) {
        let wasError = false;
        event.preventDefault();

        if (changePasswordModel.value && newPasswordModel.value != newPasswordAgainModel.value) {
            messageValueMain.value = "Введен неверный повторный пароль!"
            wasError = true;
        }

        if (deviceNameModel.value.trim().length < 4) {
            messageValueMain.value = "Длина имени устройства должна быть не менее 4 символов!"
            wasError = true;
        }

        let newPassword = newPasswordModel.value;
        if (!changePasswordModel.value) {
            newPassword = passwordModel.value;
        }

        let ports = {};
        for (let key in sensors) {
            if (sensors[key].name.trim().length < 4) {
                messageValueSensors[key] = "Длина имени устройства должна быть не менее 4 символов!"
                wasError = true;
            }

            ports[key] = {
                "enabled": sensors[key].enabled,
                "name": sensors[key].name === "" ? `Датчик ${key}` : sensors[key].name,
                "low_level_boundary": sensors[key].low_level_boundary,
                "medium_level_boundary": sensors[key].medium_level_boundary,
            };
        }

        if (wasError == true) {
            return;
        } 

        try {
            await axios.put('/api/devices/config', {
                deviceToken: props.deviceToken,
                password: passwordModel.value,
                new_password: newPassword,
                config: {
                    name: deviceNameModel.value === "" ? `Без имени` : deviceNameModel.value,
                    "ports": ports
                }
            });
            
            router.push('/');

        } catch (error) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 404:
                        console.log('Ресурс не найден:', error.response.data);
                        messageValueLast.value = "Устройство не найдено"
                        break;
                    case 401:
                        console.log('Неверный пароль:', error.response.data);
                        messageValueLast.value = "Неверный пароль"
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


    async function getConfig() {
        try {
            const response = await axios.post('/api/devices/config', {
                deviceToken: props.deviceToken
            });
            
            deviceNameModel.value = response.data.name;

            for (let key in response.data.ports) {
                messageValueSensors.push("");
                sensors[key] = ({
                    name: response.data.ports[key].name,
                    low_level_boundary: response.data.ports[key].low_level_boundary,
                    medium_level_boundary: response.data.ports[key].medium_level_boundary,
                    enabled: response.data.ports[key].enabled,
                });
            }

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

            router.push('/');
        }
    }

    onMounted(async () => {
        await getConfig();
    });

</script>


<style scoped>
    h1 {
        font-family: "Montserrat";
        color: #113259;
        margin-bottom: 48px;
        text-align: center;
    }

    form {
        display: flex;
        flex-direction: column;
        gap: 32px;
    }

    input[type="text"], input[type="number"], input[type="password"] {
        font-family: "Montserrat";
        width: 433px;
        height: 53px;
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 20px;
        border: none;
        padding-left: 12px;
        padding-right: 12px;
        margin-right: 16px;   
    }
    

    input[type="checkbox"] {
        width: 40px;
        height: 40px;
    }

    label {
        margin: 0px;
        color: #113259;
        font-family: "Montserrat";
        font-weight: 600;
        font-size: 22px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .settings-submit-button {
        font-family: "Montserrat";
        background-color: #8AB73F;
        width: 149px;
        height: 53px;
        color: #fff;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    .settings-submit-button:hover {
        background-color: #7ea83a;
    }
    
    .settings-submit-button-wrapper {
        display: flex;

    }

    .settings-wrapper {
        background-color: #EBF5FB;
        padding: 32px;
        margin-top: 24px;
        border-radius: 20px;
        margin-bottom: 48px;
    }

    .message {
        font-family: "Montserrat";
        font-size: 20px;
        margin-bottom: 16px;
        margin-top: 16px;
        font-weight: 500;
        color: #f04848;
    }

    .config-block {
        border: 3px solid #959292;
        padding: 24px;
        border-radius: 10px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 24px;
        row-gap: 36px;
    }

    .config-block legend {
        font-size: 20px;
        font-family: "Montserrat";
        font-weight: 500;
    }

    .checkbox_label {
        flex-direction: row;
        align-items: center
    }

    .config-main {
        flex-direction: column;
    }

    .new-password-block {
        display: flex;
        flex-direction: row;
        gap: 24px;
    }

    @media (max-width: 576px) {
        h1 {
            margin-bottom: 32px;
            font-size: 18px;
        }

        form {
            gap: 24px;
        }

        input[type="text"], input[type="number"], input[type="password"] {
            width: 90%;
            height: 28px;
            font-size: 14px;
            padding-left: 12px;
            padding-right: 12px;
            margin-right: 16px;   
            border-radius: 6px;
        }
        

        input[type="checkbox"] {
            width: 25px;
            height: 25px;
        }

        label {
            margin: 0px;
            font-size: 14px;
            gap: 10px;
        }

        .settings-submit-button {
            width: 100px;
            height: 33px;
            font-size: 14px;
            border-radius: 8px;
        }


        .settings-wrapper {
            padding: 20px;
            margin-top: 16px;
            border-radius: 20px;
            margin-bottom: 48px;
        }

        .message {
            font-size: 14px;
            margin-bottom: 6px;
            margin-top: 6px;
        }

        .config-block {
            padding: 24px;
            gap: 24px;
            row-gap: 18px;
        }

        .config-block legend {
            font-size: 16px;
        }

        .new-password-block {
            gap: 24px;
            flex-direction: column;
        }

    }
</style>
