import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage/MainPage.vue';
import RegistrationPage from '../components/RegistrationPage/RegistrationPage.vue';
import SettingsPage from '../components/SettingsPage/SettingsPage.vue';
import NotificationsPage from "../components/NotificationsPage/NotificationsPage.vue";
import CreateNotificationPage from "../components/CreateNotificationPage/CreateNotificationPage.vue";
import UpdateNotificationPage from "../components/UpdateNotificationPage/UpdateNotificationPage.vue"

const routes = [
    {
        path: '/',
        name: 'Home',
        component: MainPage
    },
    {
        path: '/register',
        name: 'Registration',
        component: RegistrationPage
    },
    {
        path: '/settings/:deviceToken',
        name: 'Settings',
        component: SettingsPage,
        props: true
    },
    {
        path: '/notifications/:deviceToken',
        name: 'Notifications',
        component: NotificationsPage,
        props: true
    },
    {
        path: '/notifications/create/:deviceToken',
        name: 'CreateNotifications',
        component: CreateNotificationPage,
        props: true
    },
    {
        path: '/notifications/update/:id/:deviceToken',
        name: 'UpdateNotifications',
        component: UpdateNotificationPage,
        props: true
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

