import React, { useState } from 'react'
import LegendItem from './LegendItem'
import './Legend.css'
import MapIcon from '@mui/icons-material/Map';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';

export default function Legend(): JSX.Element {
    const [isOpen, setIsOpen] = useState(true);

    if (isOpen) {
        return (
            <dialog className="Legend">
                <IconButton className="Legend-CloseButton" onClick={(): void => setIsOpen(false)}>
                    <CloseIcon />
                </IconButton>
                <ul className="Legend-List">
                    <LegendItem name="Toiletten" color="#00FF00" />
                    <LegendItem name="Trinkbrunnen" color="#2ACAEA" />
                    <LegendItem name="Tafeln" color="#FFFF00" />
                    <LegendItem name="Defibrillatoren" color="#990000" />
                </ul>
            </dialog>
        )
    } else {
        return (
            <button className="Legend--closed" onClick={(): void => setIsOpen(true)}>
                <MapIcon className="Legend-OpenButtonIcon" />
            </button>
        )
    }
}