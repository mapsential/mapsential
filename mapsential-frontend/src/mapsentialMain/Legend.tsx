import CloseIcon from '@mui/icons-material/Close';
import Box from '@mui/material/Box/Box';
import Checkbox from '@mui/material/Checkbox';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import IconButton from '@mui/material/IconButton';
import RadioGroup from '@mui/material/RadioGroup';
import { useContext, useState } from 'react';
import './Legend.css';
import { StoreContext } from './Store';

export default function Legend(): JSX.Element {
    const store = useContext(StoreContext)
    const [isOpen, setIsOpen] = useState(true);

    const formControls: JSX.Element[] = []
    for (const [locationTypeName, locationTypeEntry] of Object.entries(store.locationTypes)) {
        formControls.push(<FormControlLabel 
            key={`checkbox-${locationTypeName}`}
            value={locationTypeName}
            control={<Checkbox 
                defaultChecked={locationTypeEntry.isDisplayingMapLayer}
                onChange={() => store.toggleLocationType(locationTypeName)}
                style={{color: locationTypeEntry.cssColor}}
            />}
            label={locationTypeEntry.translations?.de.plural}
        />)
    }

    if (isOpen) {
        return (
            <dialog className="Legend">
                <IconButton className="Legend-CloseButton" onClick={(): void => setIsOpen(false)}>
                    <CloseIcon />
                </IconButton>
                {(store.locationsStatus === "loaded")
                    ? <Box className="Legend-Checkboxes" width="30%" height="30%">
                        <FormControl component="fieldset">
                            <FormLabel component="legend"></FormLabel>
                            <RadioGroup aria-label="" defaultValue="" name="radio-buttons-group">
                                {formControls}
                            </RadioGroup>
                        </FormControl>
                    </Box>
                    : <span>Loading...</span>
                }
            </dialog>
        )
    } else {
        return (
            <button className="Legend--closed" onClick={(): void => setIsOpen(true)}>
                <img src="map.svg" className="Legend-OpenButtonIcon" />
            </button>
        )
    }
}