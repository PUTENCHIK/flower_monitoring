<template>
    <label
        class="switch"
        title='Активировать/Деактивировать уведомление'>
        <input type='checkbox' v-model="internalIsUsed" />
        <span class="slider round"></span>
    </label>
</template>

<script setup>
    import { defineEmits, ref, watch, onMounted } from 'vue';

    const emit = defineEmits(['switch']);  


    const props = defineProps({
        isUsed: {
            type: Boolean,
            required: true,
        }
    });
        const internalIsUsed = ref(props.isUsed);

    watch(internalIsUsed, (newValue) => {
        emit("switch", newValue);
    });

    onMounted(() => {
        internalIsUsed.value = props.isUsed;
    });

    watch(() => props.isUsed, (newValue) => {
        internalIsUsed.value = newValue;
    });

</script>


<style scoped>
    .switch {
        position: relative;
        display: inline-block;
        width: 48.6px;
        height: 27.54px;
    }

    .switch input {
        width: 0;
        height: 0;
        opacity: 0;
    }

    .slider {
        position: absolute;
        inset: 0;
        background-color: #cccccc;
        cursor: pointer;
        transition: 0.4s;
    }

    .slider::before {
        position: absolute;
        bottom: 3px;
        left: 4px;
        width: 21.06px;
        height: 21.06px;
        background-color: white;
        transition: 0.4s;
        content: '';
    }

    input:checked + .slider {
        background-color: #8AB73F;
    }

    input:focus + .slider {
        box-shadow: 0 0 1px #8AB73F;
    }

    input:checked + .slider::before {
        transform: translateX(21px);
    }

    .slider.round {
        border-radius: 34px;
    }

    .slider.round::before {
        border-radius: 50%;
    }

</style>
