<template>
    <div class="card" :class="cardStyles">
        <img class="card__img" :src="imageSrc">
        <h3>{{ props.name }}</h3>
        <div class="humidity-wrapper">
            <span class="humidity-percentage">{{ props.humidityValue }}%</span>
            <div class="humidity-bar">
                <div :class="humidityBarStyles" :style="{ width: humidityBarWidth }"></div>
            </div>
        </div>
        <span class="card__last-update">Последнее обновление: {{ props.lastActivity }}</span>
    </div>

</template>

<script setup lang="ts">
    import { ref, defineProps, computed } from 'vue';
    import verySadPlant from '@/assets/very_sad_plant.png';
    import sadPlant from '@/assets/sad_plant.png';
    import happyPlant from '@/assets/happy_plant.png';

    const props = defineProps({
        name: {
            type: String,
            required: true,
        },
        humidityValue: {
            type: Number,
            required: true,
        },
        humidityStatus: {
            type: String,
            required: true,
            validator: (value: string) => ['low', 'medium', 'high'].includes(value),
        },
        lastActivity: {
            type: String,
            required: true,
        },
    });

    const imageSrc = computed(() => {
        switch (props.humidityStatus) {
            case 'low':
                return verySadPlant;
            case 'medium':
                return sadPlant;
            case 'high':
                return happyPlant;
        }
    });

    const cardStyles = computed(() => ({
        'card': true,
        'card--low': props.humidityStatus === 'low',
        'card--medium': props.humidityStatus === 'medium',
        'card--high': props.humidityStatus === 'high',
    }));

    const humidityBarStyles = computed(() => ({
        'humidity-bar__progress': true,
        'humidity-bar__progress--low': props.humidityStatus === 'low',
        'humidity-bar__progress--medium': props.humidityStatus === 'medium',
        'humidity-bar__progress--high': props.humidityStatus === 'high',
    }));

    const humidityBarWidth = computed(() => {
        return props.humidityValue + "%";
    });

</script>


<style scoped>
    .card {
        width: 413px;
        height: 540px;
        border-radius: 38px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 24px;
        box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
    }

    .card--low {
        background-color: #9A7960;
    }

    .card--medium {
        background-color: #AEAF63;
    }

    .card--high {
        background-color: #629A60;
    }

    h3 {
        font-family: "Montserrat";
        font-size: 24px;
        color: #fff;
        margin: 0px;
    }

    .humidity-wrapper {
        display: flex;
        flex-direction: row;
        gap: 16px;
    }

    .humidity-percentage {
        font-family: "Montserrat";
        font-size: 24px;
        color: #fff;
        font-weight: 500;
    }

    .humidity-bar {
        width: 250px;
        height: 27px;
        border-radius: 10px;
        background-color: #686868;
    }

    .humidity-bar__progress {
        height: 100%;
        border-radius: 10px;
    }

    .humidity-bar__progress--low {
        background-color: #B76F3F;
    }

    .humidity-bar__progress--medium {
        background-color: #CAC845;
    }

    .humidity-bar__progress--high {
        background-color: #8AB73F;
    }

    .card__last-update {
        font-family: "Montserrat";
        font-size: 16px;
        color: #fff;
        margin-top: 16px;
    }
</style>
