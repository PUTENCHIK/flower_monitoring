<template>
    <div class="content">
        <div class="settings-wrapper">
            <h1>Настройка устройства</h1>
            <form @submit="changeConfig">
                <div class="config-block config-main">
                    <label>
                        Имя устройства:
                        <br>
                        <input v-model="deviceNameModel" type="text" name="" placeholder="Введите имя устройства">
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
                            <input required v-model="newPasswordModel" type="password" name="" placeholder="Введите новый пароль устройства">
                        </label>
                        <label>
                            Повторно введите новый пароль: 
                            <br>
                            <input required v-model="newPasswordAgainModel" type="password" name="" placeholder="Введите новый пароль устройства">
                        </label>
                    </div>
                    
                </div>

                <fieldset v-for="(sensor, index) in sensors" :key="index" class="config-block">
                    <legend>Датчик {{ index }}</legend>
                    <label>
                        Имя датчика:
                        <br>
                        <input v-model="sensor.name" type="text" placeholder="Введите имя датчика">
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
                </fieldset>

                <label>
                    Введите пароль для подтвердения:
                    <br>
                    <input required v-model="passwordModel" type="password" name="" placeholder="Введите пароль устройства">
                </label>

                <span class="message"> {{ messageValue }}</span>
                <div class="settings-submit-button-wrapper">
                    <button class="settings-submit-button" type="submit">Отправить</button>
                </div>
  
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
    import axios from 'axios';
    import { reactive, ref, onMounted } from 'vue';
    import { useRouter } from 'vue-router';
    

    const router = useRouter()

    interface Port {
        name: string,
        low_level_boundary: number,
        medium_level_boundary: number,
        enabled: boolean,
    }

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

    const sensors = reactive<{ [index: string]: Port}>({});
    const messageValue = ref("");


    async function changeConfig(event: Event) {
        event.preventDefault();

        if (changePasswordModel.value && newPasswordModel.value != newPasswordAgainModel.value) {
            messageValue.value = "Введен неверный повторный пароль!"
        }

        let newPassword = newPasswordModel.value;
        if (!changePasswordModel.value) {
            newPassword = passwordModel.value;
        }

        let ports: { [index: string]: Port } = {};
        for (let key in sensors) {
            ports[key] = {
                "enabled": sensors[key].enabled,
                "name": sensors[key].name === "" ? `Датчик ${key}` : sensors[key].name,
                "low_level_boundary": sensors[key].low_level_boundary,
                "medium_level_boundary": sensors[key].medium_level_boundary,
            };
        }

        try {
            await axios.put('http://localhost:5050/devices/config', {
                deviceToken: props.deviceToken,
                password: passwordModel.value,
                new_password: newPassword,
                config: {
                    name: deviceNameModel.value === "" ? `Без имени` : deviceNameModel.value,
                    "ports": ports
                }
            });
            
            router.push('/');

        } catch (error: any) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 404:
                        console.log('Ресурс не найден:', error.response.data);
                        messageValue.value = "Устройство не найдено"
                        break;
                    case 401:
                        console.log('Неверный пароль:', error.response.data);
                        messageValue.value = "Неверный пароль"
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
            const response = await axios.post('http://localhost:5050/devices/config', {
                deviceToken: props.deviceToken
            });
            
            deviceNameModel.value = response.data.name;

            for (let key in response.data.ports) {
                sensors[key] = ({
                    name: response.data.ports[key].name,
                    low_level_boundary: response.data.ports[key].low_level_boundary,
                    medium_level_boundary: response.data.ports[key].medium_level_boundary,
                    enabled: response.data.ports[key].enabled,
                });
            }

        } catch (error: any) {
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
</style>
