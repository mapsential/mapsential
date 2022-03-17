import { useContext, useState } from 'react'
import './Legend.css'
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box/Box';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import { locationTypeColors, locationTypeNames, locationTypesSortedByNames } from './Constants';
import Checkbox from '@mui/material/Checkbox';
import { StoreContext } from './Store';
import { LocationType } from './Types';
import FormControlLabel from '@mui/material/FormControlLabel';

export default function Legend(): JSX.Element {
    const store = useContext(StoreContext)
    const [isOpen, setIsOpen] = useState(true);

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
                                {locationTypesSortedByNames.map((locationType: LocationType): JSX.Element => <FormControlLabel 
                                    key={`checkbox-${locationType}`}
                                    value={locationType}
                                    control={<Checkbox 
                                        defaultChecked={store.locationTypes[locationType].isDisplayingMapLayer}
                                        onChange={(_, isChecked) => store.toggleLocationType(locationType)}
                                        style={{color: locationTypeColors[locationType]}}
                                    />}
                                    label={locationTypeNames[locationType].plural}
                                />)}
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