package com.memberservice.entity;

import com.fasterxml.jackson.annotation.*;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.GenericGenerator;
import java.util.UUID;

@Entity
@Table(name = "tblMember")
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
public class Member {

    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Column(name = "id", updatable = false, nullable = false)
    private UUID id;

    @Column(name = "username", unique = true, nullable = false)
    private String username;

    @Column(name = "password", nullable = false)
    @JsonIgnore  // Không serialize password
    private String password;

    @Column(name = "email", unique = true, nullable = false)
    private String email;

    @Column(name = "phoneNumber")
    private String phoneNumber;

    @Column(name = "department")
    private String department;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "tblFullNameId")
    @JsonProperty("fullName")
    private FullName fullName;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "tblRoleId")
    @JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})
    private Role role;
}