<template>
    <div class="content notification-content">
        <div class="create-wrapper">
            <div>
                <img class="back" src="@/assets/arrow.png" @click="() => router.go(-1)">
                <h1>Редактирование уведомления</h1>
            </div>
            <form @submit="handleSubmit">
                <label>
                    Сообщение уведомления:
                    <br>
                    <input minlength="4" maxlength="40" @change="inputChange" v-model="notifyMessageModel" type="text" name="" id="" placeholder="Введите сообщение">
                </label>
                <label>
                    Время отправки уведомления:
                    <br>
                    <input @change="inputChange" v-model="notifyTimeModel" type="time" name="" id="">
                </label>
                <div class="day-selector">
                    <label class="day-selector__label">Выберите дни недели:</label>
                    <div class="day-selector__days-container">
                        <button
                            type="button"
                            v-for="(day, index) in daysOfWeek"
                            :key="index"
                            :class="{
                                'day-selector__day': true,
                                'day-selector__day--selected': selectedDays.includes(day.value),
                            }"
                            @click="toggleDay(day.value)"
                        >
                            {{ day.label }}
                        </button>
                    </div>
                </div>
                <label>
                    Пароль устройства:
                    <br>
                    <input minlength="4" maxlength="40" v-model="passwordModel" type="password" name="" id="" placeholder="Введите пароль устройства">
                </label>
                <span class="message"> {{ messageValue }}</span>
                <div class="create-submit-button-wrapper">
                    <button class="create-submit-button" type="submit">Отправить</button>
                </div>

            </form>
        </div>
    </div>

</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router';

    const daysOfWeek = ref([
        { label: 'Пн', value: 'monday', bit: 1 },
        { label: 'Вт', value: 'tuesday', bit: 2 },
        { label: 'Ср', value: 'wednesday', bit: 4 },
        { label: 'Чт', value: 'thursday', bit: 8 },
        { label: 'Пт', value: 'friday', bit: 16 },
        { label: 'Сб', value: 'saturday', bit: 32 },
        { label: 'Вс', value: 'sunday', bit: 64 },
    ]);

    const props = defineProps({
        deviceToken: {
            type: String,
            required: true,
        },
        id: {
            type: Number,
            required: true,
        }
    });
    const router = useRouter();

    const selectedDays = ref([]);
    const notifyMessageModel = ref("");
    const notifyTimeModel = ref("");
    const passwordModel = ref("");
    const messageValue = ref("");
    const isActive = ref(false);

    const toggleDay = (dayValue) => {
        if (selectedDays.value.includes(dayValue)) {
            selectedDays.value = selectedDays.value.filter((day) => day !== dayValue);
        } else {
            selectedDays.value.push(dayValue);
        }
    };

    function inputChange() {
        messageValue.value = ""
    }

    function calculateDayOfWeekSum(days) {
        const dayValues = {
            'monday': 1,
            'tuesday': 2,
            'wednesday': 4,
            'thursday': 8,
            'friday': 16,
            'saturday': 32,
            'sunday': 64
        };

        let sum = 0;
        for (const day of days) {
            sum += dayValues[day];
        }

        return sum;
    }

    async function handleSubmit(event) {
        event.preventDefault();
        messageValue.value = "";
        const days = calculateDayOfWeekSum([...selectedDays.value]);

        if (notifyMessageModel.value.trim() < 5) {
            messageValue.value = "Длина сообщения должна быть не менее 4 символов!";
            return;
        }

        if (notifyTimeModel.value.trim() < 5) {
            messageValue.value = "Не указано время";
            return;
        }

        if (selectedDays.value.length === 0) {
            messageValue.value = "Не указаны дни";
            return;
        }

        try {
            const response = await axios.put('/api/notifications', {
                deviceToken: props.deviceToken,
                password: passwordModel.value,
                message: notifyMessageModel.value,
                days: parseInt(days),
                time: notifyTimeModel.value,
                isActive: isActive.value,
                notification_id: props.id
            });

            console.log('Успешный ответ:', response.data);
            router.go(-1);
            return;

        } catch (error) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 400:
                        messageValue.value = "Такой уведомление уже есть"
                        break;
                    case 401:
                        messageValue.value = "Неверный пароль"
                        break;
                    case 404:
                        messageValue.value = "Такое устройство не найдено"
                        break;
                    case 422:
                        messageValue.value = "Неверно заполнены поля"
                        break;
                    default:
                        messageValue.value = "Неизвестная ошибка"
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

    async function getNofitification() {
        try {
            const response = await axios.post('/api/notifications/find', {
                deviceToken: props.deviceToken,
                notification_id: props.id
            });

            console.log(response.data.data);
            notifyMessageModel.value = response.data.data.message;
            notifyTimeModel.value = response.data.data.time;
            isActive.value = response.data.data.isActive;
            daysOfWeek.value.forEach(day => {
                if ((response.data.data.days & day.bit) !== 0) {
                    selectedDays.value.push(day.value);
                }
            });

            console.log(selectedDays.value);

        } catch (error) {
            console.log('Ошибка при запросе:', error);

            if (error.response) {
                switch (error.response.status) { 
                    case 400:
                        messageValue.value = "Такой уведомление уже есть"
                        break;
                    case 404:
                        messageValue.value = "Такое уведомление не найдено"
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

    onMounted(async () => {
        await getNofitification();
    });
</script>


<style scoped>
    .notification-content {
        display: flex;
        justify-content: center;
    }

    .create-wrapper {
        background-color: #EBF5FB;
        padding: 32px;
        margin-top: 24px;
        border-radius: 20px;
        margin-bottom: 48px;
        width: 60%;
    }

    h1 {
        font-family: "Montserrat";
        color: #113259;
        margin-bottom: 48px;
        text-align: center;
        font-size: 25px;
    }


    form {
        display: flex;
        flex-direction: column;
        gap: 28px;
    }

    input[type="text"], input[type="password"], input[type="time"] {
        font-family: "Montserrat";
        width: 433px;
        height: 46px;
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
        color: #113259;
        font-family: "Montserrat";
        font-weight: 600;
        font-size: 18px;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .create-submit-button {
        font-family: "Montserrat";
        background-color: #8AB73F;
        width: 150px;
        height: 45px;
        color: #fff;
        border-radius: 10px;
        font-size: 18px;
        cursor: pointer;
        border: none;
    }

    .create-submit-button:hover {
        background-color: #7ea83a;
    }
    
    .create-submit-button-wrapper {
        display: flex;

    }

    .message {
        font-family: "Montserrat";
        font-size: 18px;
        margin-bottom: 16px;
        margin-top: 16px;
        font-weight: 500;
        color: #f04848;
    }

    .back {
        width: 26px;
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .back:hover {
        background-color: #eaeaea;
        box-shadow: 0px 5px 10px 2px rgba(34, 60, 80, 0.2);
    }

    .day-selector {
        font-family: sans-serif;
        width: 100%;
        max-width: 500px;
        padding: 8px 0px;
        border-radius: 8px;
    }

    .day-selector__label {
        display: block;
        margin-bottom: 10px;
        font-weight: bold;
    }

    .day-selector__days-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 15px;
    }

    .day-selector__day {
        padding: 8px 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        background-color: #fff;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        font-size: 0.9rem;
    }

    /* .day-selector__day:hover {
        background-color: #f0f0f0;
    } */

    .day-selector__day--selected {
        background-color: #4CAF50;
        color: white;
        border-color: #4CAF50;
    }

    .day-selector__submit-button:hover {
        background-color: #0056b3;
    }

    .day-selector__selected-days {
        margin-top: 15px;
        font-style: italic;
        color: #777;
    }


    @media (max-width: 576px) {
        h1 {
            margin-bottom: 32px;
            font-size: 18px;
            margin-top: 24px;
        }

        .back {
            display: none;
        }

        input[type="text"], input[type="password"], input[type="time"] {
            width: 243px;
            height: 43px;
            font-size: 15px;
        }

        label {
            font-size: 16px;
        }

        .day-selector {
            padding: 0px;
        }

        .day-selector__days-container {
            margin: 8px 0px;
        }

        .message {
            font-size: 16px;
            margin-bottom: 8px;
            margin-top: 8px;
        }

        .create-submit-button {
            width: 129px;
            height: 43px;
            font-size: 16px;
        }

        .create-wrapper {
            width: 100%;
        }
    }
</style>

