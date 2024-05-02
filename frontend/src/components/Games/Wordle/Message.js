import React from "react";
import Alert from "react-bootstrap/Alert"


export default function Message({ message }) {
    const [show, setShow] = React.useState(true);

    if (show) {
        return (
            <Alert
            variant="warning"
            onClose={() => setShow(false)}
            className="py-1 px-2 m-0"
            style={{maxWidth: "300px", fontSize: "small"}}>
                {message}
            </Alert>
        );
    } else {
        return null;
    }
}