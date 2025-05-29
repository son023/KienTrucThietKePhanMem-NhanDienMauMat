package com.memberservice.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import java.util.UUID;

@Entity
@Table(name = "tblFullName")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FullName {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Column(name = "firstName")
    @JsonProperty("firstName")
    private String firstName;

    @Column(name = "lastName")
    @JsonProperty("lastName")
    private String lastName;

}