
const API_BASE_URL = '/api';

export const getHealth = async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
};

export const getUsers = async (status = '') => {
    let url = `${API_BASE_URL}/users`;
    if (status) {
        url += `?status=${status}`;
    }
    const response = await fetch(url);
    return response.json();
};

export const approveUser = async (userId, approve) => {
    const response = await fetch(`${API_BASE_URL}/users/approve_user`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, approve: approve }),
    });
    return response.json();
};

export const changeUserLevel = async (userId, level) => {
    const response = await fetch(`${API_BASE_URL}/users/change_level?user_id=${userId}&level=${level}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    });
    return response.json();
};

export const publishContent = async (title, body, link, levels) => {
    const response = await fetch(`${API_BASE_URL}/contents/publish_content`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, body, link, levels }),
    });
    return response.json();
};

export const getHistory = async () => {
    const response = await fetch(`${API_BASE_URL}/contents/history`);
    return response.json();
};

export const deleteUser = async (userId) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        method: 'DELETE',
    });
    return response.json();
};

export const sendNotification = async (contentId, level) => {
    const response = await fetch(`${API_BASE_URL}/contents/send_notification`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content_id: contentId, level: level }),
    });
    return response.json();
};

export const updateUser = async (userId, userData) => {
    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });
    return response.json();
};

export const login = async (password) => {
    const response = await fetch(`${API_BASE_URL}/users/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password }),
    });
    return response.json();
};
