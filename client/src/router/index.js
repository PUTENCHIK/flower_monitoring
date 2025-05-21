import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage/MainPage.vue';
import RegistrationPage from '../components/RegistrationPage/RegistrationPage.vue';
import SettingsPage from '../components/SettingsPage/SettingsPage.vue';

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
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;

