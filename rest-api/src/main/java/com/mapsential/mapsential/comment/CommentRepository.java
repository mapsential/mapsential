package com.mapsential.mapsential.comment;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface CommentRepository extends JpaRepository<CommentResource, Long> {

    @Query(value = "SELECT * FROM comments WHERE detail_id ?1", nativeQuery = true)
    List<CommentResource> findAllCommentsByDetailID(String detailId);

}
