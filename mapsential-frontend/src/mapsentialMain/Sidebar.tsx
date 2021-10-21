import React, {useContext} from 'react'
import {Box, Checkbox, FormControl, FormControlLabel, FormLabel, RadioGroup} from "@mui/material";
import {CheckboxContext} from "./MapsentialMain";

export default function Sidebar() {
    const checkboxes = useContext(CheckboxContext)
    return (
        <Box width="30%" height="30%">
            <h1>Filter</h1>
            <FormControl component="fieldset">
                <FormLabel component="legend"></FormLabel>
                <RadioGroup
                    aria-label=""
                    defaultValue=""
                    name="radio-buttons-group"
                >
                    <FormControlLabel value="Drinking Fountain" control={<Checkbox defaultChecked={checkboxes.c1}
                                                                                   onChange={(event, isChecked) => {
                                                                                       checkboxes.setC1(isChecked)
                                                                                   }}/>} label="drinking_fountain"/>
                    <FormControlLabel value="Soup Kitchen" control={<Checkbox defaultChecked={checkboxes.c1}
                                                                              onChange={(event, isChecked) => {
                                                                                  checkboxes.setC2(isChecked)
                                                                              }}/>} label="soup_kitchen"/>
                    <FormControlLabel value="Toilet" control={<Checkbox defaultChecked={checkboxes.c1}
                                                                        onChange={(event, isChecked) => {
                                                                            checkboxes.setC3(isChecked)
                                                                        }}/>} label="toilet"/>
                </RadioGroup>
            </FormControl>
        </Box>
    )
}