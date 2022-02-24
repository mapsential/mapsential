import React, {useContext} from 'react'
import {Box, Checkbox, FormControl, FormControlLabel, FormLabel, RadioGroup} from "@mui/material";
import {StoreContext} from "./Store";
import {locationTypeColors, locationTypeNames, locationTypesSortedByNames} from './Constants';
import { LocationType } from './Types';

export default function Sidebar() {
    const store = useContext(StoreContext)
    return (
        <Box width="30%" height="30%">
            <h1>Filter</h1>
            <FormControl component="fieldset">
                <FormLabel component="legend"></FormLabel>
                <RadioGroup aria-label="" defaultValue="" name="radio-buttons-group">
                    {locationTypesSortedByNames.map((locationType: LocationType): JSX.Element => <FormControlLabel 
                        key={`checkbox-${locationType}`}
                        value={locationType}
                        control={<Checkbox 
                            defaultChecked={store[locationType].status !== "unchecked"}
                            onChange={(_, isChecked) => store[locationType].setStatus(isChecked ? "loaded" : "unchecked")}
                            style={{color: locationTypeColors[locationType]}}
                        />}
                        label={locationTypeNames[locationType].plural}
                    />)}
                </RadioGroup>
            </FormControl>
        </Box>
    )
}