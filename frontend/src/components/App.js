import React from 'react';
import { createRoot } from "react-dom/client";


function App() {
    return (
        <div>
            <h1>Hello world</h1>
        </div>
    );
}

const appDiv = document.querySelector("#app");
const root = createRoot(appDiv);
root.render(
    <App />
);