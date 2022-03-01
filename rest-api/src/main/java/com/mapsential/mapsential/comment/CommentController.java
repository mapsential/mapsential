package com.mapsential.mapsential.comment;

import io.swagger.v3.oas.annotations.parameters.RequestBody;
import lombok.NoArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@CrossOrigin(origins = "*", allowedHeaders = "*")
@NoArgsConstructor
@RestController

public class CommentController {
    @Autowired
    CommentService commentService;

    @Autowired
    CommentRepository commentRepository;

    @PostMapping(value = "/api/comment")
    public void addComment(@RequestBody CommentResource newComment){
        newComment.setTimestamp(System.currentTimeMillis());
        commentService.addComment(newComment);
    }

    @GetMapping(value = "/api/comment", produces = "application/json")
    public List<CommentResource> getAllCommentsByDetailId(String detailId){
        return commentService.getAllCommentsByDetailId(detailId);
    }

}
