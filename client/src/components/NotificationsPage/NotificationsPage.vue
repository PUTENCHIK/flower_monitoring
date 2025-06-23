<template>
    <div class="content">
        <div class="notifications-wrapper">
            <img class="back" src="@/assets/arrow.png" @click="() => router.go(-1)">
            <h1>Настройка уведомлений</h1>
            <div class="add-notification-wrapper">
                <div></div>
                <router-link :to="{ name: 'CreateNotifications', params: { deviceToken: props.deviceToken} }">
                    <button class="add-notification" type="submit">Создать новое уведомление</button>
                </router-link>
            </div>
            <div class="notifications">
                <p v-if="loading" class="loading-text">Загрузка уведомлений...</p>
                <p v-else-if="error" class="error-text">{{ error }}</p>
                <p v-else-if="notifications.length === 0" class="empty-list-text">Уведомлений пока не добавлено.</p>
                <table v-else>
                    <thead>
                        <tr>
                            <th>Сообщение</th>
                            <th>Дни недели</th>
                            <th>Время</th>
                            <th>Активность</th>
                            <th>Функции</th>
                        </tr>
                    </thead>
                    <tbody>
                        <NotificationItem v-for="(item) in notifications"
                            :key="item.id"
                            :notification="item"
                            :deviceToken="props.deviceToken"
                            @refresh-data="handleRefreshData"
                        />
                    </tbody>
                </table>
            </div>

        </div>

    </div>
</template>

<script setup>
    import NotificationItem from './NotificationItem.vue';
    import axios from 'axios';
    import { onMounted, reactive, ref } from 'vue';
    import { useRouter } from 'vue-router';
    const loading = ref(false);
    const error = ref(null);
    const router = useRouter()


    let notifications = reactive([]);

    const props = defineProps({
        deviceToken: {
            type: String,
            required: true,
        }
    });

    async function getNotifications() {
        loading.value = true;
        error.value = null;
        notifications = [];

        try {
            const response = await axios.post('/api/notifications/list', {
                deviceToken: props.deviceToken
            });

            console.log('Успешный ответ:', response.data);

            response.data.data.forEach(notification => {
                const weekdays = [];
                const days = notification.days;
                
                if (days & 1) {
                    weekdays.push("Понедельник");
                }
                if (days & 2) {
                    weekdays.push("Вторник");
                }
                if (days & 4) {
                    weekdays.push("Среда");
                }
                if (days & 8) {
                    weekdays.push("Четверг");
                }
                if (days & 16) {
                    weekdays.push("Пятница");
                }
                if (days & 32) {
                    weekdays.push("Суббота");
                }
                if (days & 64) {
                    weekdays.push("Воскресенье");
                }

                notifications.push({
                    id: notification.id,
                    message: notification.message,
                    days: weekdays.toString().replaceAll(',', ', '),
                    time: notification.time, 
                    isActive: notification.isActive
                })
            });

            // notifications.splice(0, notifications.length, ...response.data.data);
        } catch (e) {
            let errorMessage = 'Неизвестная ошибка при получении уведомлений.';
            if (e instanceof Error) {
                errorMessage = `Ошибка при получении уведомлений: ${e.message}`;
            }
            console.error(errorMessage, e);
            error.value = errorMessage;

        } finally {
            loading.value = false;
        }
    }

    async function handleRefreshData() {
        await getNotifications();
    }

    onMounted(async () => {
        await getNotifications();
    });
</script>


<style scoped>
    h1 {
        font-family: "Montserrat";
        color: #113259;
        margin-bottom: 48px;
        text-align: center;
        font-size: 25px;
    }

    .notifications-wrapper {
        background-color: #EBF5FB;
        padding: 32px;
        margin-top: 24px;
        border-radius: 20px;
        margin-bottom: 48px;
    }

    .notifications-wrapper table {
        width: 100%;
    }

    .notifications-wrapper th {
        padding: 16px 24px;
        color: #616161;
        font-weight: 500;
        font-style: normal;
        text-align: left;
        user-select: none;
    }

    .notifications td {
        height: 100%;
        padding: 16px 24px;
        border-top: 1px solid #b7b7b7;
    }

    .notifications {
        box-sizing: border-box;
        width: 100%;
        padding: 24px;
        background-color: #ffffff;
        border-radius: 16px;
        font-family: "Montserrat";
    }

    .add-notification {
        font-family: "Montserrat";
        background-color: #113259;
        color: #fff;
        border-radius: 10px;
        padding: 11px 16px;
        font-size: 16px;
        cursor: pointer;
        border: none;
        margin-bottom: 24px;
    }

    .add-notification-wrapper {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
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

    @media (max-width: 576px) {
        h1 {
            margin-bottom: 32px;
            font-size: 18px;
            margin-top: 24px;
        }

       .back {
            display: none;
        }

        .notifications {
            overflow-x: scroll;
            position: relative;
        }

        .notifications-wrapper {
            padding: 16px 0px;
        }

        .add-notification {
            font-size: 14px;
        }

        .add-notification-wrapper {
            justify-content: center;
        }

        .add-notification-wrapper div {
            display: none;
        }

        .notifications-wrapper th {
            font-size: 14px;
        }

    }
</style>
