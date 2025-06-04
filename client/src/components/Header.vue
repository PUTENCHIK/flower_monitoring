<template>
    <header>
        <div class="content header-content">
            <router-link to="/">
                <div class="logo-wrapper">
                    <img class="logo" src="@/assets/plant-pot.png" alt="Лого">
                    <span class="logo-name">Flower Monitoring</span>
                </div>
            </router-link>  

            <router-link to="/register">
                <button class="button-register" type="button">Зарегистрировать</button>
            </router-link>
            
        </div>
    </header>

</template>

<script setup >
    
</script>


<style scoped>
    header {
        background-color: #fff;
        height: 80px;
    }

    .header-content {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        height: 100%;
    }

    .header-content > a {
        text-decoration: none;
    }

    .logo {
        width: 50px;
        height: 50px;
        margin-right: 12px;
    }

    .logo-name {
        font-family: "Montserrat";
        font-weight: 500;
        font-size: 24px;
        text-decoration: none;
        color: black;
    }

    .logo-wrapper {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .button-register {
        font-family: "Montserrat";
        background-color: #8AB73F;
        width: 199px;
        height: 53px;
        color: #fff;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    .button-register:hover {
        background-color: #7ea83a;
    }

    @media (max-width: 576px) {
        header {
            height: 70px;
        }

        .header-content {
            justify-content: space-around;
        }

        .logo {
            width: 30px;
            height: 30px;
            margin-right: 6px;
        }
        .logo-name {
            font-size: 16px;
        }

        .button-register {
            width: 136px;
            height: 40px;
            font-size: 13px;
        }
    }

</style>
