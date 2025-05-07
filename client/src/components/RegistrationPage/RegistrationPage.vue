<template>
    <div class="content">
        <div class="register-wrapper">
            <h1>Регистрация устройства</h1>
            <form @submit="register">
                <label>
                    Токен устройства:
                    <br>
                    <input @change="inputChange" v-model="tokenModel" type="text" name="" id="" placeholder="Введите токен устройства">
                </label>
                <label>
                    Пароль устройства:
                    <br>
                    <input v-model="passwordModel" type="text" name="" id="" placeholder="Введите пароль устройства">
                </label>
                <span class="message"> {{ messageValue }}</span>
                <div class="register-submit-button-wrapper">
                    <button class="register-submit-button" type="submit">Отправить</button>
                </div>

            </form>
        </div>
    </div>

</template>

<script setup lang="ts">
    import axios from 'axios';
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

    const router = useRouter()

    const tokenModel = ref("");
    const passwordModel = ref("");
    const messageValue = ref("");

    async function register(event: Event) {
        event.preventDefault();
        messageValue.value = "";

        try {
            const response = await axios.post('http://localhost:5050/devices/register', {
                deviceToken: tokenModel.value,
                password: passwordModel.value
            });

            console.log('Успешный ответ:', response.data);

            let checkTokens = localStorage.getItem("deviceTokens");
            let tokens: string[] = [];
            if (checkTokens !== null) {
                tokens = JSON.parse(checkTokens)
            }

            tokens.push(tokenModel.value);
            localStorage.setItem("deviceTokens", JSON.stringify(tokens));
            router.push('/');
            return;

        } catch (error: any) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 400:
                        console.log('Ресурс уже зарегистрирован:', error.response.data);
                        messageValue.value = "Устройство уже зарегистрировано"
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

    function inputChange() {
        messageValue.value = ""
    }
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

    input {
        font-family: "Montserrat";
        width: 433px;
        height: 53px;
        background-color: #ffffff;
        border-radius: 10px;
        font-size: 18px;
        border: none;
        padding-left: 12px;
        padding-right: 12px;
        margin-right: 16px;
        
    }

    label {
        margin: 0px;
        /* color: #113259; */
        font-family: "Montserrat";
        font-weight: 600;
        font-size: 22px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .register-submit-button {
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

    .register-submit-button:hover {
        background-color: #7ea83a;
    }
    
    .register-submit-button-wrapper {
        display: flex;

    }

    .register-wrapper {
        background-color: #EBF5FB;
        padding: 32px;
        margin-top: 24px;
        border-radius: 20px;
    }

    .message {
        font-family: "Montserrat";
        font-size: 20px;
        margin-bottom: 16px;
        margin-top: 16px;
        font-weight: 500;
        color: #f04848;
    }

</style>
