import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import React, { useContext } from "react"
import Comments from "./Comments"
import { StoreContext } from "./Store"


export default function CommentDialog()  {
    const store = useContext(StoreContext)
    const handleClose = () => {
        store.setCommentsAreOpen(false)
    }

    if (store.commentsAreOpen && store.currentCommentLocation === null) {
        console.error("'currentCommentLocation' should be set!")
    }

    return(
        <div>
            <Dialog 
                open={store.commentsAreOpen} 
                onClose={handleClose}
            >
                <DialogTitle>Kommentare</DialogTitle>
                <DialogContent>
                    {store.currentCommentLocation !== null
                        ? <Comments location={store.currentCommentLocation} />
                        : <p>
                            Die Kommentare könnten nicht geöffnet werden. <br />
                            Bitte kontaktieren Sie unsere Entwicklerteam.
                        </p> 
                    }
                </DialogContent>
            </Dialog>
        </div>
    )
}