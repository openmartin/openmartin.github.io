Title: multiple tiles containers
Status: published
Date: 2020-07-09 17:00
Modified: 2020-07-09 17:00
Category: Java
Tags: java
Slug: multi-tiles-containers
Authors: Martin
Summary: 使用 multiple container 实现 同一套代码，不同的站点，不同的样式


其实使用 spring mvc theme 也可以实现同样的需求，不过还是用 tiles multiple container 更加灵活一些。

## multiple-containers

https://tiles.apache.org/framework/tutorial/advanced/multiple-containers.html


一套代码，多个site显示不一样

1. 新增一个 Servlet Filter：通过 request 的域名来判断是那个站点，request.setAttribute
2. 多个 tiles container
3. 新建 tilesView，通过站点来判断，用不同的 tiles container 来输出
4. 加载 definition 的时候修改来实现不同的站点不同的 definition

### SiteFilter

```java
public class SiteFilter implements Filter {

    public static final String SITE_FILTER_ATTRIBUTE = "SITE_FILTER_ATTRIBUTE";

    public static final String EXAMPLE1_SITE = "example1";
    public static final String EXAMPLE2_SITE = "example2";

    public static final String EXAMPLE1_SITE_DOMAIN = "example1.com";
    public static final String EXAMPLE2_SITE_DOMAIN = "example2.com";

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        if (request.getAttribute("SITE_FILTER_ATTRIBUTE") != null) {
            chain.doFilter(request, response);
        } else {
            String site = null;
            if (request.getServerName().equals(EXAMPLE1_SITE_DOMAIN)){
                site = EXAMPLE1_SITE;
            } else if (request.getServerName().equals(EXAMPLE2_SITE_DOMAIN)) {
                site = EXAMPLE2_SITE;
            }

            if (site == null) {
                site = request.getParameter("site");
            }

            if (EXAMPLE1_SITE.equals(site)) {
                request.setAttribute(SITE_FILTER_ATTRIBUTE, EXAMPLE1_SITE);
            } else if (EXAMPLE2_SITE.equals(site)){
                request.setAttribute(SITE_FILTER_ATTRIBUTE, EXAMPLE2_SITE);
            } else { // 默认是 EXAMPLE1_SITE
                request.setAttribute(SITE_FILTER_ATTRIBUTE, EXAMPLE1_SITE);
            }

            chain.doFilter(request, response);
        }
    }

    @Override
    public void destroy() {

    }
}
```

### SiteTilesView

把默认的 `org.springframework.web.servlet.view.tiles3.TilesView` 替换为自己写的 `SiteTilesView`

```
<bean id="viewResolver" class="org.springframework.web.servlet.view.UrlBasedViewResolver">
    <property name="viewClass">
        <value>
            com.example.web.tiles.SiteTilesView
        </value>
    </property>
</bean>
```

在 TilesView 上修改，根据 filter 中设置的 SITE_FILTER_ATTRIBUTE，使用不同的 Tiles Container 来 render。

```java
public class SiteTilesView extends AbstractUrlBasedView {

    private Map<String, Renderer> siteRendererMap;

    private boolean exposeJstlAttributes = true;

    private boolean alwaysInclude = false;

    private ApplicationContext applicationContext;


    /**
     * Whether to expose JSTL attributes. By default set to {@code true}.
     *
     * @see JstlUtils#exposeLocalizationContext(RequestContext)
     */
    protected void setExposeJstlAttributes(boolean exposeJstlAttributes) {
        this.exposeJstlAttributes = exposeJstlAttributes;
    }

    /**
     * Specify whether to always include the view rather than forward to it.
     * <p>Default is "false". Switch this flag on to enforce the use of a
     * Servlet include, even if a forward would be possible.
     *
     * @see TilesViewResolver#setAlwaysInclude
     * @since 4.1.2
     */
    public void setAlwaysInclude(boolean alwaysInclude) {
        this.alwaysInclude = alwaysInclude;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        super.afterPropertiesSet();

        ServletContext servletContext = getServletContext();
        Assert.state(servletContext != null, "No ServletContext");
        this.applicationContext = ServletUtil.getApplicationContext(servletContext);

        if (this.siteRendererMap == null) {
            siteRendererMap = new HashMap<>(4);
            TilesContainer defaultContainer = TilesAccess.getContainer(this.applicationContext);
            Renderer defaultRenderer = new DefinitionRenderer(defaultContainer);

            siteRendererMap.put("example1", defaultRenderer);

            TilesContainer fiContainer = TilesAccess.getContainer(this.applicationContext, "example2");
            Renderer fiRenderer = new DefinitionRenderer(fiContainer);

            siteRendererMap.put("example2", fiRenderer);
        }
    }

    @Override
    public boolean checkResource(final Locale locale) throws Exception {
        Assert.state(this.siteRendererMap != null, "No Renderer set");

        HttpServletRequest servletRequest = null;
        RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
        if (requestAttributes instanceof ServletRequestAttributes) {
            servletRequest = ((ServletRequestAttributes) requestAttributes).getRequest();
        }

        String site = (String) requestAttributes.getAttribute(SiteFilter.SITE_FILTER_ATTRIBUTE, RequestAttributes.SCOPE_REQUEST);

        Request request = new ServletRequest(this.applicationContext, servletRequest, null) {
            @Override
            public Locale getRequestLocale() {
                return locale;
            }
        };

        Renderer renderer = siteRendererMap.get(site);
        return renderer.isRenderable(getUrl(), request);
    }

    @Override
    protected void renderMergedOutputModel(Map<String, Object> model, HttpServletRequest request, HttpServletResponse response) throws Exception {
        Assert.state(this.siteRendererMap != null, "No Renderer set");

        exposeModelAsRequestAttributes(model, request);
        if (this.exposeJstlAttributes) {
            JstlUtils.exposeLocalizationContext(new RequestContext(request, getServletContext()));
        }
        if (this.alwaysInclude) {
            request.setAttribute(AbstractRequest.FORCE_INCLUDE_ATTRIBUTE_NAME, true);
        }

        String site = (String) request.getAttribute(SiteFilter.SITE_FILTER_ATTRIBUTE);

        Request tilesRequest = createTilesRequest(request, response);

        Renderer renderer = siteRendererMap.get(site);
        renderer.render(getUrl(), tilesRequest);
    }

    /**
     * Create a Tiles {@link Request}.
     * <p>This implementation creates a {@link ServletRequest}.
     *
     * @param request  the current request
     * @param response the current response
     * @return the Tiles request
     */
    protected Request createTilesRequest(final HttpServletRequest request, HttpServletResponse response) {
        return new ServletRequest(this.applicationContext, request, response) {
            @Override
            public Locale getRequestLocale() {
                return RequestContextUtils.getLocale(request);
            }
        };
    }
}
```

### SiteSpringTilesConfigurer

系统默认的 `org.springframework.web.servlet.view.tiles3.TilesConfigurer` 只能初始化一个 default 的 container，新建一个 `SiteSpringTilesConfigurer`

```java
public class SiteSpringTilesConfigurer implements ServletContextAware, InitializingBean, DisposableBean {

    private static final boolean tilesElPresent =
            ClassUtils.isPresent("org.apache.tiles.el.ELAttributeEvaluator", SiteSpringTilesConfigurer.class.getClassLoader());


    protected final Log logger = LogFactory.getLog(getClass());

    private TilesInitializer tilesInitializer;

    private String[] definitions;

    private boolean checkRefresh = false;

    private boolean validateDefinitions = true;

    private Class<? extends DefinitionsFactory> definitionsFactoryClass;

    private Class<? extends PreparerFactory> preparerFactoryClass;

    private boolean useMutableTilesContainer = false;

    private ServletContext servletContext;

    private String containerKey;


    /**
     * Configure Tiles using a custom TilesInitializer, typically specified as an inner bean.
     * <p>Default is a variant of {@link org.apache.tiles.startup.DefaultTilesInitializer},
     * respecting the "definitions", "preparerFactoryClass" etc properties on this configurer.
     * <p><b>NOTE: Specifying a custom TilesInitializer effectively disables all other bean
     * properties on this configurer.</b> The entire initialization procedure is then left
     * to the TilesInitializer as specified.
     */
    public void setTilesInitializer(TilesInitializer tilesInitializer) {
        this.tilesInitializer = tilesInitializer;
    }

    /**
     * Set the Tiles definitions, i.e. the list of files containing the definitions.
     * Default is "/WEB-INF/tiles.xml".
     */
    public void setDefinitions(String... definitions) {
        this.definitions = definitions;
    }

    /**
     * Set whether to check Tiles definition files for a refresh at runtime.
     * Default is "false".
     */
    public void setCheckRefresh(boolean checkRefresh) {
        this.checkRefresh = checkRefresh;
    }

    /**
     * Set whether to validate the Tiles XML definitions. Default is "true".
     */
    public void setValidateDefinitions(boolean validateDefinitions) {
        this.validateDefinitions = validateDefinitions;
    }

    /**
     * Set the {@link org.apache.tiles.definition.DefinitionsFactory} implementation to use.
     * Default is {@link org.apache.tiles.definition.UnresolvingLocaleDefinitionsFactory},
     * operating on definition resource URLs.
     * <p>Specify a custom DefinitionsFactory, e.g. a UrlDefinitionsFactory subclass,
     * to customize the creation of Tiles Definition objects. Note that such a
     * DefinitionsFactory has to be able to handle {@link java.net.URL} source objects,
     * unless you configure a different TilesContainerFactory.
     */
    public void setDefinitionsFactoryClass(Class<? extends DefinitionsFactory> definitionsFactoryClass) {
        this.definitionsFactoryClass = definitionsFactoryClass;
    }

    /**
     * Set the {@link org.apache.tiles.preparer.factory.PreparerFactory} implementation to use.
     * Default is {@link org.apache.tiles.preparer.factory.BasicPreparerFactory}, creating
     * shared instances for specified preparer classes.
     * <p>Specify {@link SimpleSpringPreparerFactory} to autowire
     * {@link org.apache.tiles.preparer.ViewPreparer} instances based on specified
     * preparer classes, applying Spring's container callbacks as well as applying
     * configured Spring BeanPostProcessors. If Spring's context-wide annotation-config
     * has been activated, annotations in ViewPreparer classes will be automatically
     * detected and applied.
     * <p>Specify {@link SpringBeanPreparerFactory} to operate on specified preparer
     * <i>names</i> instead of classes, obtaining the corresponding Spring bean from
     * the DispatcherServlet's application context. The full bean creation process
     * will be in the control of the Spring application context in this case,
     * allowing for the use of scoped beans etc. Note that you need to define one
     * Spring bean definition per preparer name (as used in your Tiles definitions).
     *
     * @see SimpleSpringPreparerFactory
     * @see SpringBeanPreparerFactory
     */
    public void setPreparerFactoryClass(Class<? extends PreparerFactory> preparerFactoryClass) {
        this.preparerFactoryClass = preparerFactoryClass;
    }

    /**
     * Set whether to use a MutableTilesContainer (typically the CachingTilesContainer
     * implementation) for this application. Default is "false".
     *
     * @see org.apache.tiles.mgmt.MutableTilesContainer
     * @see org.apache.tiles.impl.mgmt.CachingTilesContainer
     */
    public void setUseMutableTilesContainer(boolean useMutableTilesContainer) {
        this.useMutableTilesContainer = useMutableTilesContainer;
    }

    @Override
    public void setServletContext(ServletContext servletContext) {
        this.servletContext = servletContext;
    }

    public void setContainerKey(String containerKey) {
        this.containerKey = containerKey;
    }

    /**
     * Creates and exposes a TilesContainer for this web application,
     * delegating to the TilesInitializer.
     *
     * @throws TilesException in case of setup failure
     */
    @Override
    public void afterPropertiesSet() throws TilesException {
        ApplicationContext preliminaryContext = new SpringWildcardServletTilesApplicationContext(this.servletContext);
        if (this.tilesInitializer == null) {
            this.tilesInitializer = new SiteSpringTilesInitializer();
        }
        this.tilesInitializer.initialize(preliminaryContext);
    }

    /**
     * Removes the TilesContainer from this web application.
     *
     * @throws TilesException in case of cleanup failure
     */
    @Override
    public void destroy() throws TilesException {
        this.tilesInitializer.destroy();
    }

    private static class CompositeELResolverImpl extends CompositeELResolver {

        public CompositeELResolverImpl() {
            add(new ScopeELResolver());
            add(new TilesContextELResolver(new TilesContextBeanELResolver()));
            add(new TilesContextBeanELResolver());
            add(new ArrayELResolver(false));
            add(new ListELResolver(false));
            add(new MapELResolver(false));
            add(new ResourceBundleELResolver());
            add(new BeanELResolver(false));
        }
    }

    private class SiteSpringTilesInitializer extends DefaultTilesInitializer {

        @Override
        protected String getContainerKey(
                ApplicationContext applicationContext) {
            return containerKey;
        }

        @Override
        protected AbstractTilesContainerFactory createContainerFactory(ApplicationContext context) {
            return new SiteSpringTilesContainerFactory();
        }
    }

    private class SiteSpringTilesContainerFactory extends BasicTilesContainerFactory {

        @Override
        protected TilesContainer createDecoratedContainer(TilesContainer originalContainer, ApplicationContext context) {
            return (useMutableTilesContainer ? new CachingTilesContainer(originalContainer) : originalContainer);
        }

        @Override
        protected List<ApplicationResource> getSources(ApplicationContext applicationContext) {
            if (definitions != null) {
                List<ApplicationResource> result = new LinkedList<ApplicationResource>();
                for (String definition : definitions) {
                    Collection<ApplicationResource> resources = applicationContext.getResources(definition);
                    if (resources != null) {
                        result.addAll(resources);
                    }
                }
                return result;
            } else {
                return super.getSources(applicationContext);
            }
        }

        @Override
        protected BaseLocaleUrlDefinitionDAO instantiateLocaleDefinitionDao(ApplicationContext applicationContext,
                                                                            LocaleResolver resolver) {
            BaseLocaleUrlDefinitionDAO dao = new ModifyDefinitionDAO(applicationContext);
            if (checkRefresh && dao instanceof CachingLocaleUrlDefinitionDAO) {
                ((CachingLocaleUrlDefinitionDAO) dao).setCheckRefresh(true);
            }
            return dao;
        }

        @Override
        protected DefinitionsReader createDefinitionsReader(ApplicationContext context) {
            DigesterDefinitionsReader reader = (DigesterDefinitionsReader) super.createDefinitionsReader(context);
            reader.setValidating(validateDefinitions);
            return reader;
        }

        @Override
        protected DefinitionsFactory createDefinitionsFactory(ApplicationContext applicationContext,
                                                              LocaleResolver resolver) {

            if (definitionsFactoryClass != null) {
                DefinitionsFactory factory = BeanUtils.instantiate(definitionsFactoryClass);
                if (factory instanceof ApplicationContextAware) {
                    ((ApplicationContextAware) factory).setApplicationContext(applicationContext);
                }
                BeanWrapper bw = PropertyAccessorFactory.forBeanPropertyAccess(factory);
                if (bw.isWritableProperty("localeResolver")) {
                    bw.setPropertyValue("localeResolver", resolver);
                }
                if (bw.isWritableProperty("definitionDAO")) {
                    bw.setPropertyValue("definitionDAO", createLocaleDefinitionDao(applicationContext, resolver));
                }
                return factory;
            } else {
                return super.createDefinitionsFactory(applicationContext, resolver);
            }
        }

        @Override
        protected PreparerFactory createPreparerFactory(ApplicationContext context) {
            if (preparerFactoryClass != null) {
                return BeanUtils.instantiate(preparerFactoryClass);
            } else {
                return super.createPreparerFactory(context);
            }
        }

        @Override
        protected LocaleResolver createLocaleResolver(ApplicationContext context) {
            return new SpringLocaleResolver();
        }

        @Override
        protected AttributeEvaluatorFactory createAttributeEvaluatorFactory(ApplicationContext context,
                                                                            LocaleResolver resolver) {
            AttributeEvaluator evaluator;
            if (tilesElPresent && JspFactory.getDefaultFactory() != null) {
                evaluator = new TilesElActivator().createEvaluator();
            } else {
                evaluator = new DirectAttributeEvaluator();
            }
            return new BasicAttributeEvaluatorFactory(evaluator);
        }
    }

    private class TilesElActivator {

        public AttributeEvaluator createEvaluator() {
            ELAttributeEvaluator evaluator = new ELAttributeEvaluator();
            evaluator.setExpressionFactory(
                    JspFactory.getDefaultFactory().getJspApplicationContext(servletContext).getExpressionFactory());
            evaluator.setResolver(new CompositeELResolverImpl());
            return evaluator;
        }
    }
}
```

ModifyDefinitionDAO 中修改 tiles.xml 定义，也可以 load 一个新的xml 来覆盖 tiles.xml 中的定义

```java
public class ModifyDefinitionDAO extends ResolvingLocaleUrlDefinitionDAO {

    public ModifyDefinitionDAO(ApplicationContext applicationContext) {
        super(applicationContext);
    }

    @Override
    protected Map<String, Definition> loadDefinitionsFromResource(ApplicationResource resource) {
        Map<String, Definition> defsMap = super.loadDefinitionsFromResource(resource);

        // modify DefinitionDAO
        if (defsMap != null) {
            modifyDefinition(defsMap);
        }
        return defsMap;
    }


    protected void modifyDefinition(Map<String, Definition> defsMap) {
        // modify login
        Definition loginDefinition = defsMap.get("login");
        loginDefinition.getTemplateAttribute().setValue("/WEB-INF/jsp/example2login.jsp");

        // modify baselayout
        Definition layoutDefinition = defsMap.get("baselayout");
        layoutDefinition.getTemplateAttribute().setValue("/WEB-INF/jsp/example2layout.jsp");
    }

}
```

## 结论

以上代码可以完成目标，不过感觉不够灵活，不知道除了 theme 以外是否还有其他方案。