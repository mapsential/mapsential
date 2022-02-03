package com.mapsential.mapsential.comment;


import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.lang.Nullable;

import javax.persistence.*;
import java.io.Serializable;

@NoArgsConstructor
@AllArgsConstructor
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@Entity
@Table(name = "comments")
public class CommentResource implements Serializable {

    @Id
    @Column(name = "id")
    private Long commentId;

    @ManyToOne
    @JoinColumn(name = "details_id")
    private Long detailId;

    @Column(name = "author_name")
    private Long authorName;

    @Column(name = "content")
    private Long content;

//    @Nullable
    @Column(name = "timestamp")
    private Long timestamp;



}
