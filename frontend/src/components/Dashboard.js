import React from 'react';
import Users from './Users';

const Dashboard = ({ onLogout }) => {
    return (
        <div className="bg-white rounded-lg shadow-md w-full max-w-6xl h-full max-h-screen overflow-hidden flex flex-col">
            <nav className="bg-gray-800 text-white p-4 flex justify-end">
                <button
                    onClick={onLogout}
                    className="px-4 py-2 bg-red-600 rounded hover:bg-red-700"
                >
                    Logout
                </button>
            </nav>
            <div className="p-6 overflow-auto">
                <Users />
            </div>
        </div>
    );
};

export default Dashboard;
