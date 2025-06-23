<template>
    <div v-if="isVisible" class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h3>Введите пароль</h3>
                <button @click="closeModal" class="close-button">&times;</button>
            </div>
            <div class="modal-body">
                <input
                type="password"
                v-model="password"
                placeholder="Пароль"
                @keyup.enter="submitPassword"
                />
            </div>
            <div class="modal-footer">
                <button @click="submitPassword" class="submit-button">Подтвердить</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
    isVisible: {
        type: Boolean,
        required: true
    }
});

const emit = defineEmits(['close', 'submit']);

const password = ref('');

watch(() => props.isVisible, (newValue) => {
    if (newValue) {
        password.value = '';
    }
});


const closeModal = () => {
    emit('close');
};

const submitPassword = () => {
    emit('submit', password.value);
    closeModal();
};
</script>

<style scoped>

    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        font-family: "Montserrat";
    }

    .modal {
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        width: 400px;
        overflow: hidden;
    }

    .modal-header {
        padding: 15px;
        background-color: #f0f0f0;
        border-bottom: 1px solid #ddd;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .modal-header h3 {
        margin: 0;
        font-size: 18px;
    }

    .close-button {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }

    .modal-body {
        padding: 20px;
    }

    .modal-body input {
        width: 80%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 1rem;
        font-family: inherit;
    }

    .modal-footer {
        padding: 15px;
        background-color: #f0f0f0;
        border-top: 1px solid #ddd;
        text-align: right;
    }

    .submit-button {
        background-color: #8AB73F;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 1rem;
        font-family: inherit;
    }

    .submit-button:hover {
        background-color: #3e8e41;
    }
</style>