<template>
    <div class="device-section" :style="{backgroundColor: props.backgroundColor}">
        
        <div class="content header-content">
            <div class="title-wrapper">
                <h2>Устройство: {{ props.name }}</h2>
                <router-link to="/settings">
                    <img class="settings" src="@/assets/settings.svg" alt="settings">
                </router-link>
                <img class="delete" src="@/assets/unseen.png" alt="delete">
            </div>
            <div class="cards">
                <Card name="Cactus Danny" :humidityValue="50" humidityStatus="medium" lastActivity="23.04.2025 11:04" />
                <Card name="Cactus Maxy" :humidityValue="80" humidityStatus="high" lastActivity="23.04.2025 11:06" />
                <Card name="Cactus Glebby" :humidityValue="10" humidityStatus="low" lastActivity="23.04.2025 11:06" />
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
    import Card from "./Card.vue"
    import { defineProps } from 'vue';

    const props = defineProps({
        backgroundColor: {
            type: String,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },

    });
                
    // });



</script> 

<style scoped>
    .delete {
        width: 32px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .device-section {
        padding-top: 24px;
        padding-bottom: 32px;
    }

    .title-wrapper {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
        margin-bottom: 32px;
    }

    .settings {
        width: 32px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .settings:hover, .delete:hover {
        background-color: #eaeaea;
        box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
    }

    h2 {
        margin: 0px;
        color: #113259;
        font-family: "Montserrat";
        font-weight: 600;
    }

    .cards {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;

    }
</style>
