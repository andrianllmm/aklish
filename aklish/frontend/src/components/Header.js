import React from "react";
import LanguageSelect from "./LanguageSelect";


export default function Header({ title }) {
    return (
        <div className="container pb-3 mb-3 border-bottom d-flex align-items-center flex-wrap">
            <div className="me-auto">
                <h1>{title}</h1>
            </div>
            <LanguageSelect />
        </div>
    );
}