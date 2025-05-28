-- Tạo cơ sở dữ liệu member_management_db
CREATE DATABASE member_management_db;

-- Kết nối đến CSDL vừa tạo
\c member_management_db;

-- Cài đặt extension cho UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tạo bảng tblRole với UUID
CREATE TABLE tblRole (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    roleName varchar(50) NOT NULL,
    des varchar(255) NULL
);

-- Tạo bảng tblFullName với UUID
CREATE TABLE tblFullName (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    firstName varchar(50) NOT NULL,
    lastName varchar(50) NOT NULL
);

-- Tạo bảng tblMember với UUID
CREATE TABLE tblMember (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username varchar(50) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    phoneNumber varchar(20),
    email varchar(100),
    department varchar(100),
    tblRoleId UUID,
    tblFullNameId UUID
);

-- Tạo bảng tblEyeRecognitionModel với UUID
CREATE TABLE tblEyeRecognitionModel (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    eyeModelName varchar(100) NOT NULL,
    modelLink varchar(255) NOT NULL,
    accuracy float NOT NULL,
    f1Score float NOT NULL,
    precision float NOT NULL,
    imageSize integer NOT NULL,
    epochs integer NOT NULL,
    learningRate float NOT NULL,
    batchSize integer NOT NULL,
    mappingLabel Text NOT NULL,
    isActive boolean DEFAULT true,
    trainingTime integer,
    createDate timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng tblEyeRecognitionSample với UUID
CREATE TABLE tblEyeRecognitionSample (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memberId UUID NOT NULL,
    eyeImageLink varchar(255) NOT NULL,
    label varchar(255) NOT NULL,
    isActive boolean DEFAULT true,
    captureDate timestamp DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng tblEyeRecognitionSampleHistory với UUID và notes
CREATE TABLE tblEyeRecognitionSampleHistory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    modelId UUID NOT NULL,
    sampleId UUID NOT NULL,
    notes varchar(255)
);

-- Tạo bảng tblRecognitionEvent với UUID
CREATE TABLE tblRecognitionEvent (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    imageLink varchar(255) NOT NULL,
    recognitionModelId UUID NOT NULL,
    eyeDetectionModelId UUID NOT NULL,
    cameraName varchar(100) NOT NULL,
    timeVerify timestamp DEFAULT CURRENT_TIMESTAMP,
    isSuccessful boolean DEFAULT false,
    accuracy float,
    tblMemberId UUID
);

-- Tạo khóa ngoại
ALTER TABLE tblMember 
    ADD CONSTRAINT fk_role_id 
    FOREIGN KEY (tblRoleId) 
    REFERENCES tblRole(id);

ALTER TABLE tblMember 
    ADD CONSTRAINT fk_fullname_id 
    FOREIGN KEY (tblFullNameId) 
    REFERENCES tblFullName(id);

ALTER TABLE tblEyeRecognitionSample 
    ADD CONSTRAINT fk_member_sample_id 
    FOREIGN KEY (memberId) 
    REFERENCES tblMember(id);

ALTER TABLE tblEyeRecognitionSampleHistory 
    ADD CONSTRAINT fk_history_model_id 
    FOREIGN KEY (modelId) 
    REFERENCES tblEyeRecognitionModel(id);

ALTER TABLE tblEyeRecognitionSampleHistory 
    ADD CONSTRAINT fk_history_sample_id 
    FOREIGN KEY (sampleId) 
    REFERENCES tblEyeRecognitionSample(id);

ALTER TABLE tblRecognitionEvent 
    ADD CONSTRAINT fk_event_member_id 
    FOREIGN KEY (tblMemberId) 
    REFERENCES tblMember(id);

-- Thêm dữ liệu Role (chỉ có role Nhân viên)
INSERT INTO tblRole (id, roleName, des) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Nhân viên', 'Nhân viên thông thường');

-- Thêm dữ liệu FullName cho 40 nhân viên
INSERT INTO tblFullName (id, firstName, lastName) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'Nguyễn', 'Văn An'),
('550e8400-e29b-41d4-a716-446655440002', 'Trần', 'Thị Bình'),
('550e8400-e29b-41d4-a716-446655440003', 'Lê', 'Hoàng Cường'),
('550e8400-e29b-41d4-a716-446655440004', 'Phạm', 'Minh Dương'),
('550e8400-e29b-41d4-a716-446655440005', 'Hoàng', 'Thu Hà'),
('550e8400-e29b-41d4-a716-446655440006', 'Ngô', 'Văn Giáp'),
('550e8400-e29b-41d4-a716-446655440007', 'Đỗ', 'Thị Hồng'),
('550e8400-e29b-41d4-a716-446655440008', 'Vũ', 'Đức Hùng'),
('550e8400-e29b-41d4-a716-446655440009', 'Nguyễn', 'Thị Lan'),
('550e8400-e29b-41d4-a716-446655440010', 'Trần', 'Văn Khánh'),
('550e8400-e29b-41d4-a716-446655440011', 'Lê', 'Thị Linh'),
('550e8400-e29b-41d4-a716-446655440012', 'Phạm', 'Văn Minh'),
('550e8400-e29b-41d4-a716-446655440013', 'Hoàng', 'Thị Ngọc'),
('550e8400-e29b-41d4-a716-446655440014', 'Ngô', 'Đức Phong'),
('550e8400-e29b-41d4-a716-446655440015', 'Đỗ', 'Thu Quỳnh'),
('550e8400-e29b-41d4-a716-446655440016', 'Vũ', 'Văn Sơn'),
('550e8400-e29b-41d4-a716-446655440017', 'Nguyễn', 'Thị Tâm'),
('550e8400-e29b-41d4-a716-446655440018', 'Trần', 'Đức Thắng'),
('550e8400-e29b-41d4-a716-446655440019', 'Lê', 'Thu Uyên'),
('550e8400-e29b-41d4-a716-446655440020', 'Phạm', 'Văn Vũ'),
('550e8400-e29b-41d4-a716-446655440021', 'Hoàng', 'Thị Xuân'),
('550e8400-e29b-41d4-a716-446655440022', 'Ngô', 'Văn Yên'),
('550e8400-e29b-41d4-a716-446655440023', 'Đỗ', 'Thị Ánh'),
('550e8400-e29b-41d4-a716-446655440024', 'Vũ', 'Đức Bách'),
('550e8400-e29b-41d4-a716-446655440025', 'Nguyễn', 'Thị Châu'),
('550e8400-e29b-41d4-a716-446655440026', 'Trần', 'Văn Đạt'),
('550e8400-e29b-41d4-a716-446655440027', 'Lê', 'Thị Giang'),
('550e8400-e29b-41d4-a716-446655440028', 'Phạm', 'Văn Hiếu'),
('550e8400-e29b-41d4-a716-446655440029', 'Hoàng', 'Thị Khánh'),
('550e8400-e29b-41d4-a716-446655440030', 'Ngô', 'Đức Lâm'),
('550e8400-e29b-41d4-a716-446655440031', 'Đỗ', 'Thu Mai'),
('550e8400-e29b-41d4-a716-446655440032', 'Vũ', 'Văn Nam'),
('550e8400-e29b-41d4-a716-446655440033', 'Nguyễn', 'Thị Oanh'),
('550e8400-e29b-41d4-a716-446655440034', 'Trần', 'Đức Phúc'),
('550e8400-e29b-41d4-a716-446655440035', 'Lê', 'Thu Quế'),
('550e8400-e29b-41d4-a716-446655440036', 'Phạm', 'Văn Sáng'),
('550e8400-e29b-41d4-a716-446655440037', 'Hoàng', 'Thị Thảo'),
('550e8400-e29b-41d4-a716-446655440038', 'Ngô', 'Văn Trung'),
('550e8400-e29b-41d4-a716-446655440039', 'Đỗ', 'Thị Vân'),
('550e8400-e29b-41d4-a716-446655440040', 'Vũ', 'Đức Xương');

-- Thêm dữ liệu Member cho 40 nhân viên
INSERT INTO tblMember (id, username, password, phoneNumber, email, department, tblRoleId, tblFullNameId) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'nguyenan', 'pass123', '0901234567', 'nguyenan@company.com', 'Phòng Kế toán', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440001'),
('550e8400-e29b-41d4-a716-446655440002', 'tranbinh', 'pass123', '0901234568', 'tranbinh@company.com', 'Phòng Nhân sự', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440002'),
('550e8400-e29b-41d4-a716-446655440003', 'lecuong', 'pass123', '0901234569', 'lecuong@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440003'),
('550e8400-e29b-41d4-a716-446655440004', 'phamduong', 'pass123', '0901234570', 'phamduong@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440004'),
('550e8400-e29b-41d4-a716-446655440005', 'hoangha', 'pass123', '0901234571', 'hoangha@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440005'),
('550e8400-e29b-41d4-a716-446655440006', 'ngogiap', 'pass123', '0901234572', 'ngogiap@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440006'),
('550e8400-e29b-41d4-a716-446655440007', 'dohong', 'pass123', '0901234573', 'dohong@company.com', 'Phòng Marketing', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440007'),
('550e8400-e29b-41d4-a716-446655440008', 'vuhung', 'pass123', '0901234574', 'vuhung@company.com', 'Phòng IT', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440008'),
('550e8400-e29b-41d4-a716-446655440009', 'nguyenlan', 'pass123', '0901234575', 'nguyenlan@company.com', 'Phòng Kế toán', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440009'),
('550e8400-e29b-41d4-a716-446655440010', 'trankhanh', 'pass123', '0901234576', 'trankhanh@company.com', 'Phòng Nhân sự', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440010'),
('550e8400-e29b-41d4-a716-446655440011', 'lelinh', 'pass123', '0901234577', 'lelinh@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440011'),
('550e8400-e29b-41d4-a716-446655440012', 'phamminh', 'pass123', '0901234578', 'phamminh@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440012'),
('550e8400-e29b-41d4-a716-446655440013', 'hoangngoc', 'pass123', '0901234579', 'hoangngoc@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440013'),
('550e8400-e29b-41d4-a716-446655440014', 'ngophong', 'pass123', '0901234580', 'ngophong@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440014'),
('550e8400-e29b-41d4-a716-446655440015', 'doquynh', 'pass123', '0901234581', 'doquynh@company.com', 'Phòng Marketing', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440015'),
('550e8400-e29b-41d4-a716-446655440016', 'vuson', 'pass123', '0901234582', 'vuson@company.com', 'Phòng IT', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440016'),
('550e8400-e29b-41d4-a716-446655440017', 'nguyentam', 'pass123', '0901234583', 'nguyentam@company.com', 'Phòng Kế toán', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440017'),
('550e8400-e29b-41d4-a716-446655440018', 'tranthang', 'pass123', '0901234584', 'tranthang@company.com', 'Ban Giám đốc', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440018'),
('550e8400-e29b-41d4-a716-446655440019', 'leuyen', 'pass123', '0901234585', 'leuyen@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440019'),
('550e8400-e29b-41d4-a716-446655440020', 'phamvu', 'pass123', '0901234586', 'phamvu@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440020'),
('550e8400-e29b-41d4-a716-446655440021', 'hoangxuan', 'pass123', '0901234587', 'hoangxuan@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440021'),
('550e8400-e29b-41d4-a716-446655440022', 'ngoyen', 'pass123', '0901234588', 'ngoyen@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440022'),
('550e8400-e29b-41d4-a716-446655440023', 'doanh', 'pass123', '0901234589', 'doanh@company.com', 'Phòng Marketing', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440023'),
('550e8400-e29b-41d4-a716-446655440024', 'vubach', 'pass123', '0901234590', 'vubach@company.com', 'Phòng IT', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440024'),
('550e8400-e29b-41d4-a716-446655440025', 'nguyenchau', 'pass123', '0901234591', 'nguyenchau@company.com', 'Phòng Kế toán', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440025'),
('550e8400-e29b-41d4-a716-446655440026', 'trandat', 'pass123', '0901234592', 'trandat@company.com', 'Phòng Nhân sự', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440026'),
('550e8400-e29b-41d4-a716-446655440027', 'legiang', 'pass123', '0901234593', 'legiang@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440027'),
('550e8400-e29b-41d4-a716-446655440028', 'phamhieu', 'pass123', '0901234594', 'phamhieu@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440028'),
('550e8400-e29b-41d4-a716-446655440029', 'hoangkhanh', 'pass123', '0901234595', 'hoangkhanh@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440029'),
('550e8400-e29b-41d4-a716-446655440030', 'ngolam', 'pass123', '0901234596', 'ngolam@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440030'),
('550e8400-e29b-41d4-a716-446655440031', 'domai', 'pass123', '0901234597', 'domai@company.com', 'Phòng Marketing', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440031'),
('550e8400-e29b-41d4-a716-446655440032', 'vunam', 'pass123', '0901234598', 'vunam@company.com', 'Phòng IT', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440032'),
('550e8400-e29b-41d4-a716-446655440033', 'nguyenoanh', 'pass123', '0901234599', 'nguyenoanh@company.com', 'Phòng Kế toán', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440033'),
('550e8400-e29b-41d4-a716-446655440034', 'tranphuc', 'pass123', '0901234600', 'tranphuc@company.com', 'Phòng Nhân sự', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440034'),
('550e8400-e29b-41d4-a716-446655440035', 'leque', 'pass123', '0901234601', 'leque@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440035'),
('550e8400-e29b-41d4-a716-446655440036', 'phamsang', 'pass123', '0901234602', 'phamsang@company.com', 'Phòng Kỹ thuật', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440036'),
('550e8400-e29b-41d4-a716-446655440037', 'hoangthao', 'pass123', '0901234603', 'hoangthao@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440037'),
('550e8400-e29b-41d4-a716-446655440038', 'ngotrung', 'pass123', '0901234604', 'ngotrung@company.com', 'Phòng Kinh doanh', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440038'),
('550e8400-e29b-41d4-a716-446655440039', 'dovan', 'pass123', '0901234605', 'dovan@company.com', 'Phòng Marketing', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440039'),
('550e8400-e29b-41d4-a716-446655440040', 'vuxuong', 'pass123', '0901234606', 'vuxuong@company.com', 'Phòng IT', '550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440040');

-- Lưu ý: Dữ liệu EyeRecognitionSample sẽ được thêm sau khi upload Cloudinary
-- Sử dụng script cloudinary_uploader.py để upload ảnh và tạo SQL INSERT statements 