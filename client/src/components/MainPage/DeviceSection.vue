<template>
    <div class="device-section" :style="{backgroundColor: props.device.backgroundColor}">
        
        <div v-if="props.device" class="content header-content">
            <div class="title-wrapper">
                <div class="title-wrapper__left">
                    <h2>Устройство: {{ props.device.name }}</h2>
                    <div class="device-section__buttons">
                        <router-link :to="{ name: 'Settings', params: { deviceToken: props.device.deviceToken } }">
                            <img class="settings" src="@/assets/settings.svg" alt="settings" title="Настройки">
                        </router-link>
                        <img @click="deleteDevice" class="remove" src="@/assets/unseen.png" title="Убрать из списка" alt="remove">
                        <img @click="updateDevice" class="update" src="@/assets/refresh.png" title="Обновить" alt="update">
                    </div>
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

    
    const emit = defineEmits(['device-deleted', 'device-updated']);  

    const deleteDevice = () => {
        emit('device-deleted', props.device.deviceToken);
    };

    const updateDevice = () => {
        emit('device-updated', props.device.deviceToken);
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

    .settings:hover, .remove:hover, .update:hover {
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

    .update {
        width: 34px;
        height: 34px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .device-section__buttons {
        display: flex;
        flex-direction: row;
        gap: 16px;
        align-items: center;
    }

    @media (max-width: 576px) {
        .remove, .settings, .update {
            width: 25px;
            height: 25px;
            padding: 6px;
        }

        .device-section {
            padding-top: 24px;
            padding-bottom: 32px;
        }

        .title-wrapper {
            margin-bottom: 24px;
            flex-direction: column;
            gap: 16px;
        }

        .cards {
            gap: 20px;
        }

        .title-wrapper__left {
            gap: 12px;
            margin-right: 8px;
            margin-left: 16px;
            flex-direction: column;
        }

        .lastActivity {
            font-size: 16px;
            margin-right: 16px;
        }

        h2 {
            font-size: 18px;
        }
    }
</style>
