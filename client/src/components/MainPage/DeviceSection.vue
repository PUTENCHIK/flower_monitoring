<template>
    <div class="device-section" :style="{backgroundColor: props.device.backgroundColor}">
        
        <div v-if="props.device" class="content header-content">
            <div class="title-wrapper">
                <div class="title-wrapper__left">
                    <h2>Устройство: {{ props.device.name }}</h2>
                    <router-link :to="{ name: 'Settings', params: { deviceToken: props.device.deviceToken } }">
                        <img class="settings" src="@/assets/settings.svg" alt="settings" title="Настройки">
                    </router-link>
                    <img @click="deleteDevice" class="remove" src="@/assets/unseen.png" title="Убрать из списка" alt="remove">
                </div>

                <span class="lastActivity"> {{ props.device.lastActivity == "Данные ещё не приходили" ? props.device.lastActivity : `Обновлено: ${props.device.lastActivity}` }}</span>
            </div>
            <div class="cards">
                <Card v-for="item in props.device.ports"  
                    :name="item.name"
                    :humidityValue="item.value" 
                    :humidityState="item.state" />
            </div>
        </div>
    </div>

</template>

<script setup>
    import Card from "./Card.vue"
    import { defineProps, defineEmits, onMounted } from 'vue';

    const props = defineProps({
        device: {
            type: Object,
            required: true,
        }
    });

    

    const emit = defineEmits(['device-deleted']);  

    const deleteDevice = () => {
        emit('device-deleted', props.device.deviceToken);
    };

    onMounted(() => {
        console.log(props.device);
    });

</script> 

<style scoped>
    .remove {
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
        margin-bottom: 32px;
        justify-content: space-between;
    }

    .settings {
        width: 32px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .settings:hover, .remove:hover {
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

    .title-wrapper__left {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
    }

    .lastActivity {
        font-size: 20px;
        color: #113259;
        font-family: "Montserrat";
        font-weight: 600;
    }
</style>
