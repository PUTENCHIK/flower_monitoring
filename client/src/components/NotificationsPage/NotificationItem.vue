<template>
    <tr class="notification-row">
        <td>{{props.notification.message}}</td>
        <td>{{props.notification.days}}</td>
        <td>{{props.notification.time}}</td>
        <td v-if="props.notification.isActive" class="active">Используется</td>
        <td v-if="!props.notification.isActive" class="inactive">Не используется</td>
        <td>
            <div class="notification__functions">
                <Switch
                    :isUsed="props.notification.isActive"
                    @switch="handleChangeState"
                />
                <router-link :to="{ name: 'UpdateNotifications', params: { id: parseInt(props.notification.id), deviceToken: props.deviceToken }}">
                    <img
                        class="edit"
                        src="@/assets/pencil.png"
                        alt='Редактировать'
                        title='Редактировать'
                    />
                </router-link>
                <img
                    class="remove"
                    src="@/assets/rubbish.png"
                    @click="handleDelete"
                    alt='Удалить'
                    title='Удалить'
                />
            </div>
        </td>
    </tr>

</template>

<script setup>
    import Switch from './Switch.vue';
    import axios from 'axios';
    import { defineEmits } from 'vue';

    const emit = defineEmits(['refresh-data']);  

    const props = defineProps({
        notification: {
            type: Object,
            required: true,
        },
        deviceToken: {
            type: String,
            required: true,
        }
    });


    const handleDelete = async () => {
        try {
            const response = await axios.delete('http://localhost:5050/notifications', {
                data: {
                    deviceToken: props.deviceToken,
                    password: "password123",
                    notification_id: parseInt(props.notification.id)
                }
            });

            console.log(response);
            emit('refresh-data');
        } catch (e) {
            let errorMessage = 'Неизвестная ошибка при получении уведомлений.';
            if (e instanceof Error) {
                errorMessage = `Ошибка при получении уведомлений: ${e.message}`;
            }
            console.error(errorMessage, e);
        }
    };

    const handleChangeState = async (checked) => {
        try {
            const response = await axios.patch('http://localhost:5050/notifications/', {
                deviceToken: props.deviceToken,
                password: "password123",
                notification_id: props.notification.id,
                isActive: checked
            });

            console.log(response);

            emit('refresh-data');
        } catch (e) {
            let errorMessage = 'Неизвестная ошибка при получении уведомлений.';
            if (e instanceof Error) {
                errorMessage = `Ошибка при получении уведомлений: ${e.message}`;
            }
            console.error(errorMessage, e);
        }
    };
</script>


<style scoped>
    .active {
        color: #113259;
    }

    .inactive {
        color: #f04923;
    }

    .edit,
    .remove {
        width: 24px;
        padding: 8px;
        cursor: pointer;
    }

    .edit:hover,
    .remove:hover {
        background-color: #ffffff;
        border-radius: 8px;
    }

    .notification__functions {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 16px;
    }

    .notification-row {
        user-select: none;
    }

    .notification-row:hover {
        background-color: #e6e8e8;
    }

    .error-text_table {
        width: 200px;
    }

    .notification-row td {
        height: 100%;
        padding: 16px 24px;
        border-top: 1px solid #b7b7b7;
        font-size: 17px;
        font-weight: 500;
    }

    @media (max-width: 576px) {
        .notification-row td {
            font-size: 15px;
        }

        .edit, .remove {
            width: 22px;
            padding: 8px;
            cursor: pointer;
        }
    }

</style>
