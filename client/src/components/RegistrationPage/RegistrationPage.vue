<template>
    <div class="content">
        <div class="register-wrapper">
            <h1>Регистрация устройства</h1>
            <form action="">
                <label>
                    Токен устройства:
                    <br>
                    <input type="text" name="" id="" placeholder="Введите токен устройства">
                </label>
                <label>
                    Пароль устройства:
                    <br>
                    <input type="text" name="" id="" placeholder="Введите пароль устройства">
                </label>
                <div class="register-submit-button-wrapper">
                    <button class="register-submit-button" type="submit">Отправить</button>
                </div>

            </form>
        </div>
    </div>

</template>

<script setup lang="ts">

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
</style>
