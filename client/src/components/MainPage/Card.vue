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
    </div>

</template>

<script setup>
    import { defineProps, computed } from 'vue';
    
    import verySadPlant from '@/assets/very_sad_plant.png';
    import sadPlant from '@/assets/sad_plant.png';
    import happyPlant from '@/assets/happy_plant.png';
    import unknownPlant from '@/assets/unknown_plant.png';

    const props = defineProps({
        name: {
            type: String,
            required: true,
        },
        humidityValue: {
            type: Number,
            required: true,
        },
        humidityState: {
            type: String,
            required: true,
            validator: (value) => ['low', 'medium', 'high', 'unknown'].includes(value),
        }
    });

    const imageSrc = computed(() => {
        switch (props.humidityState) {
            case 'low':
                return verySadPlant;
            case 'medium':
                return sadPlant;
            case 'high':
                return happyPlant;
            case 'unknown':
                return unknownPlant;
        }
    });

    const cardStyles = computed(() => ({
        'card': true,
        'card--low': props.humidityState === 'low',
        'card--medium': props.humidityState === 'medium',
        'card--high': props.humidityState === 'high',
        'card--unknown': props.humidityState === 'unknown',
    }));

    const humidityBarStyles = computed(() => ({
        'humidity-bar__progress': true,
        'humidity-bar__progress--low': props.humidityState === 'low',
        'humidity-bar__progress--medium': props.humidityState === 'medium',
        'humidity-bar__progress--high': props.humidityState === 'high',
        'humidity-bar__progress--unknown': props.humidityState === 'unknown',
    }));

    const humidityBarWidth = computed(() => {
        return props.humidityValue + "%";
    });

</script>


<style scoped>
    .card {
        width: 413px;
        height: 500px;
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

    .card--unknown {
        background-color: #566573;
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

    @media (max-width: 576px) {
        .card {
            width: 90%;
            height: 410px;
            gap: 24px;
            margin: 0 auto;
        }

        .card__img {
            width: 240px;
        }

        h3 {
            font-size: 18px;
        }

        .humidity-wrapper {
            gap: 16px;
        }

        .humidity-percentage {
            font-size: 18px;
        }

        .humidity-bar {
            width: 220px;
            height: 22px;
            border-radius: 8px;
        }

    }
</style>
