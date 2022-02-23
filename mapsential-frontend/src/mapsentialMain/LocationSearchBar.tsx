import SearchBar from "material-ui-search-bar"
import List from "@mui/material/List"
import ListItem from "@mui/material/ListItem"
import { useEffect, useState } from "react"


type Suggestion = {text: string, lat: number, lon: number}


export default function LocationSearchBar(): JSX.Element {
    const [searchText, setSearchText] = useState<string>("");
    const [suggestions, setSuggestions] = useState<Suggestion[]>([])

    const handleSearchTextChange = (newText: string) => {
        setSearchText(newText)
    }

    return <div className="location-search-bar">
        <SearchBar 
            value={searchText}
            onChange={handleSearchTextChange}
        />
        <List>
            {suggestions.map((suggestion: Suggestion) => <ListItem>{suggestion.text}</ListItem>)}
        </List>
    </div>
}