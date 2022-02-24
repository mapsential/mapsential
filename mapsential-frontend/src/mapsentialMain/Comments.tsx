import {useState} from 'react'
import React from 'react'
import {CommentDetails, CommentList} from "./Types"
import {Paper, Grid} from "@mui/material";


export default function Comments({commentList}: {commentList: CommentList}) {
    const [comments, setComments] = useState<any>()
    setComments(commentList.map((comment: CommentDetails) => {
        return(
            <Grid
                container
                direction="column"
                justifyContent="center"
                alignItems="center"
            >
                <h4>{comment.authorName}</h4>
                <p>{comment.content}</p>
                <p>{comment.timestamp}</p>
            </Grid>
        )
    }))

    return(
        <div>
            <h1>asdfffsdfdf</h1>
            <Paper>
                {comments}
            </Paper>
        </div>
    )
}