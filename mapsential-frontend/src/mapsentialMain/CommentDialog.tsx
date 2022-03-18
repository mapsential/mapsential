import React from 'react'
import {useState,useContext} from 'react'
import {Dialog, DialogContent, DialogTitle} from "@mui/material";
import {StoreContext} from "./Store";
import Comments from "./Comments"


export default function CommentDialog()  {
    const store = useContext(StoreContext)
    const handleClose = () => {
        store.setCommentDialogOpen(false)
    }
    const [comments, setComments] = useState<any>()
    if(store.commentMap){
        if(store.commentMap.has(store.currentComments)){
            setComments(<Comments commentList={store.commentMap.get(store.currentComments) as any} />)
        }
    }
    return(
        <div>
            <Dialog open={store.commentDialogOpen} onClose={handleClose}>
                <DialogTitle>Kommentare</DialogTitle>
                <DialogContent>
                    {comments}
                </DialogContent>
            </Dialog>
        </div>
    )
}