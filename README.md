### Django PokeShop Project  
> 작업 완료일 : 2024/12/26  
- 개요: 포켓몬 카드게임에서 아이디어와 리소스를 가져와서 개발한 django 프로젝트입니다.  

### 구현 화면(GIF)  
![chrome-capture-2024-12-20](https://github.com/user-attachments/assets/e57f03e9-0dad-499d-8582-4ba82b4c38fa)  

### 구현 기능
- 로그인  
auth_login기능을 사용했습니다.
![image](https://github.com/user-attachments/assets/5772dfe1-2b99-4f13-af8f-d9618de2b552)  
- 회원가입  
![image](https://github.com/user-attachments/assets/389047d8-fde7-4547-8985-4f98ef999c34)  
- 상품 등록  
카드 이름, 이미지, 해시태그를 입력받습니다.
![image](https://github.com/user-attachments/assets/418f4770-75ff-450f-8e21-dfb48ffc07b0)  
- 상품 디테일  
PokeAPI를 사용해서 포켓몬 정보를 가져옵니다.  
팔로우, 찜하기가 가능합니다  
![image](https://github.com/user-attachments/assets/7f8fb8fc-cbe5-44ec-891a-013af3193dc5)  
- 상품 검색  
포켓몬 이름, 회원명 해시태그로 검색이 가능합니다.  
해당 이미지는 해시태그로 검색한 화면입니다.  
![image](https://github.com/user-attachments/assets/572e5317-86a8-4dea-a03f-eeef12c24eb8)  

### ERD 문서  
  ![image](https://github.com/user-attachments/assets/2c3803b8-1c3e-45b1-aa7c-80de5c93d10d)  

### 참고 URL  
1. 포켓몬 카드 게임 : https://pokemoncard.co.kr/main
2. PokeAPI : https://pokeapi.co/  

### 트러블 슈팅  
1. 이미지 반복 업로드  
  이미지 업로드 테스트를 하다보면 같은 이미지를 계속 올리는데  
  파일 이름이 같은 경우 파일 이름에 랜덤 값이 추가돼서 저장되는데  
  구분도 안되고 불필요하게 공간을 차지하기 때문에  
  저장할 파일의 이름을 상품의 경우 상품 ID로 설정하고  
  동일한 대상이 이미지를 업로드 할 경우 기존 파일을 삭제하고 업로드하게 해서 해결했습니다.
2. Ajax 비동기처리  
  상품 디테일 페이지에서 여러번의 ajax요청을 작성했는데
  씹히는 요청이 있었는데 Promise.all 함수를 사용해 모든 요청이  
  차례대로 처리되도록 수정했습니다.  
  또한 요청이 오래걸릴 때를 대비해서 로딩 화면을 추가했습니다.

