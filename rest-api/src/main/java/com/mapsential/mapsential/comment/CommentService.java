package com.mapsential.mapsential.comment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class CommentService {

    @Autowired
    CommentRepository commentRepository;

    public void addComment(CommentResource newComment) {
        commentRepository.save(newComment);
    }

    public List<CommentResource> getAllCommentsByDetailId(String detailId) {
        return commentRepository.findAllCommentsByDetailID(detailId);
    }
}
