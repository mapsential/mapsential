import React, {useContext} from 'react'
import {Box, Checkbox, FormControl, FormControlLabel, FormLabel, RadioGroup} from "@mui/material";
import {StoreContext} from "./Store";

export default function Sidebar() {
    const store = useContext(StoreContext)
    return (
        <Box width="30%" height="30%">
            <h1>Filter</h1>
            <FormControl component="fieldset">
                <FormLabel component="legend"></FormLabel>
                <RadioGroup aria-label="" defaultValue="" name="radio-buttons-group">
                    <FormControlLabel value="Drinking Fountain" control={<Checkbox defaultChecked={store.checkboxes.drinking_fountain_checkbox} onChange={(event, isChecked) => {store.checkboxes.setDrinking_Fountain_checkbox(isChecked)}}/>} label="Trinkbrunnen"/>
                    <FormControlLabel value="Soup Kitchen" control={<Checkbox defaultChecked={store.checkboxes.soup_Kitchen_checkbox} onChange={(event, isChecked) => {store.checkboxes.setSoup_Kitchen_checkbox(isChecked)}}/>} label="Tafeln"/>
                    <FormControlLabel value="Toilet" control={<Checkbox defaultChecked={store.checkboxes.toilet_checkbox} onChange={(event, isChecked) => {store.checkboxes.setToilet_checkbox(isChecked)}}/>} label="Toiletten"/>
                    <FormControlLabel value="Defibrilator" control={<Checkbox defaultChecked={store.checkboxes.defibrillator_checkbox} onChange={(event, isChecked) => {store.checkboxes.setDefibrillator_checkbox(isChecked)}}/>} label="Defibrillatoren"/>
                </RadioGroup>
            </FormControl>
        </Box>
    )
}