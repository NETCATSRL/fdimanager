import React, { useState, useEffect } from 'react';
import { getUsers, approveUser, changeUserLevel, deleteUser, updateUser } from '../services/api';

const Users = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [editingUser, setEditingUser] = useState(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const allUsers = await getUsers();
            const pendingUsers = await getUsers('pending');
            if (Array.isArray(allUsers) && Array.isArray(pendingUsers)) {
                const usersWithStatus = allUsers.map(u => ({
                    ...u,
                    status: pendingUsers.some(p => p.id === u.id) ? 'pending' : 'active'
                }));
                setUsers(usersWithStatus);
            } else {
                setUsers([]);
            }
        } catch (error) {
            console.error("Error fetching users:", error);
            setUsers([]);
        }
        setLoading(false);
    };

    const handleApprove = async (userId) => {
        try {
            await approveUser(userId, true);
            fetchUsers();
        } catch (error) {
            console.error("Error approving user:", error);
        }
    };

    const handleLevelChange = async (userId, level) => {
        try {
            await changeUserLevel(userId, level);
            fetchUsers();
        } catch (error) {
            console.error("Error changing user level:", error);
        }
    };

    const handleDelete = async (userId) => {
        if (window.confirm('Are you sure you want to delete this user?')) {
            try {
                await deleteUser(userId);
                fetchUsers();
            } catch (error) {
                console.error("Error deleting user:", error);
            }
        }
    };

    const handleUpdate = async (user) => {
        try {
            await updateUser(user.id, user);
            setEditingUser(null);
            fetchUsers();
        } catch (error) {
            console.error("Error updating user:", error);
        }
    };

    const filteredUsers = users.filter(user =>
        (user.first_name && user.first_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (user.last_name && user.last_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        user.telegram_id.toString().includes(searchTerm)
    );

    if (loading) {
        return <div className="text-center py-8">Loading users...</div>;
    }

    return (
        <div>
            <input
                type="text"
                placeholder="Search by name or Telegram ID"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-3 mb-4 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="overflow-x-auto">
                <table className="w-full table-auto border-collapse border border-gray-300">
                    <thead>
                        <tr className="bg-gray-100">
                            <th className="border border-gray-300 p-2">ID</th>
                            <th className="border border-gray-300 p-2">Telegram ID</th>
                            <th className="border border-gray-300 p-2">First Name</th>
                            <th className="border border-gray-300 p-2">Last Name</th>
                            <th className="border border-gray-300 p-2">Phone</th>
                            <th className="border border-gray-300 p-2">Email</th>
                            <th className="border border-gray-300 p-2">Address</th>
                            <th className="border border-gray-300 p-2">Notes</th>
                            <th className="border border-gray-300 p-2">Level</th>
                            <th className="border border-gray-300 p-2">Status</th>
                            <th className="border border-gray-300 p-2">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredUsers.map(user => (
                            <tr key={user.id} className="hover:bg-gray-50">
                                <td className="border border-gray-300 p-2">{user.id}</td>
                                <td className="border border-gray-300 p-2">{user.telegram_id}</td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <input
                                            type="text"
                                            value={editingUser.first_name || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, first_name: e.target.value })}
                                            className="w-full p-1 border rounded"
                                        />
                                    ) : (
                                        user.first_name
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <input
                                            type="text"
                                            value={editingUser.last_name || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, last_name: e.target.value })}
                                            className="w-full p-1 border rounded"
                                        />
                                    ) : (
                                        user.last_name
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <input
                                            type="text"
                                            value={editingUser.phone || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, phone: e.target.value })}
                                            className="w-full p-1 border rounded"
                                        />
                                    ) : (
                                        user.phone
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <input
                                            type="email"
                                            value={editingUser.email || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, email: e.target.value })}
                                            className="w-full p-1 border rounded"
                                        />
                                    ) : (
                                        user.email
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <input
                                            type="text"
                                            value={editingUser.indirizzo || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, indirizzo: e.target.value })}
                                            className="w-full p-1 border rounded"
                                        />
                                    ) : (
                                        user.indirizzo
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    {editingUser?.id === user.id ? (
                                        <textarea
                                            value={editingUser.varie || ''}
                                            onChange={(e) => setEditingUser({ ...editingUser, varie: e.target.value })}
                                            className="w-full p-1 border rounded"
                                            rows={2}
                                        />
                                    ) : (
                                        user.varie
                                    )}
                                </td>
                                <td className="border border-gray-300 p-2">
                                    <select
                                        value={user.level}
                                        onChange={(e) => handleLevelChange(user.id, parseInt(e.target.value))}
                                        className="p-1 border rounded"
                                    >
                                        {[1, 2, 3, 4].map(level => (
                                            <option key={level} value={level}>Level {level}</option>
                                        ))}
                                    </select>
                                </td>
                                <td className="border border-gray-300 p-2">{user.status}</td>
                                <td className="border border-gray-300 p-2 space-x-1">
                                    {user.status === 'pending' && (
                                        <button
                                            onClick={() => handleApprove(user.id)}
                                            className="px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600 text-sm"
                                        >
                                            Approve
                                        </button>
                                    )}
                                    {editingUser?.id === user.id ? (
                                        <div className="space-x-1">
                                            <button
                                                onClick={() => handleUpdate(editingUser)}
                                                className="px-2 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
                                            >
                                                Save
                                            </button>
                                            <button
                                                onClick={() => setEditingUser(null)}
                                                className="px-2 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 text-sm"
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    ) : (
                                        <button
                                            onClick={() => setEditingUser(user)}
                                            className="px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 text-sm"
                                        >
                                            Edit
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleDelete(user.id)}
                                        className="px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Users;