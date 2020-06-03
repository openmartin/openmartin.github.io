Title: spring controller 的 testcase
Status: published
Date: 2020-06-03 21:00
Modified: 2020-06-03 21:00
Category: Java
Tags: java, spring, test
Slug: test-spring-controller
Authors: Martin
Summary: 如何写 controller 的 testcase

## testcase of controller

一般情况下我们都是写 service 层的 testcase，一是因为写起来比较方便，二是因为 controller 层中的逻辑比较少

如果需要写 controller 的 testcase，spring-test 也是支持的

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration({"classpath:applicationContext.xml", "classpath:spring-mvc.xml"})
@ActiveProfiles("test")
@WebAppConfiguration
public class DemoControllerTest {

    private MockMvc mockMvc;

    ObjectMapper mapper = new ObjectMapper();

    @Autowired
    private WebApplicationContext webApplicationContext;


    @Before
    public void setUp() {
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
    }

    @Test
    public void testGetUserById() throws Exception {
        String respString = mockMvc.perform(get("/demo/user").param("userId", "ABC"))
                .andExpect(status().isOk())
                .andDo(print())
                .andReturn().getResponse().getContentAsString();
        System.out.println("return json: " + respString);
    }

    @Test
    public void testAddUser() throws Exception {
        User user = new User();
        user.setFirstName("Hello");
        user.setLastName("World");
        user.setAge(18);
        String requestJsonString = mapper.writeValueAsString(user);
        String respString = mockMvc.perform(post("/demo/user/add")
                .contentType(MediaType.APPLICATION_JSON)
                .content(requestJsonString))
                .andExpect(status().isOk())
                .andDo(print())
                .andReturn().getResponse().getContentAsString();

        System.out.println("return json: " + respString);

    }
```

### 注意事项

1. @ContextConfiguration 需要把 spring-mvc.xml 也添加进去
2. 添加 @WebAppConfiguration 参考 [@WebAppConfiguration Example](https://www.concretepage.com/spring-5/webappconfiguration-example-spring-test)
3. MockMvcBuilders.standaloneSetup(new MyController()).build() 不会自动注入依赖的 service，建议使用 MockMvcBuilders.webAppContextSetup(webApplicationContext).build()




