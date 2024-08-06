import React from "react";
import LanguageSelect from "./LanguageSelect";


export default function Header({ title }) {
    return (
        <div className="container d-flex align-items-center flex-wrap mb-3 border-bottom">
            <div className="me-auto">
                <h1>{title}</h1>
            </div>
            <LanguageSelect />
        </div>
    );
}