
# jhipster-ext

1. Create sub-packages `repository`, `service`, `service.impl` and `web.rest` under some ext, say `x` package.

3. Update App class, add the following annotations:
`
@EnableJpaRepositories("<ext repository package>")
@ComponentScan({"<base package>", "<ext package>"})
`

5. Create and extend corresponding `x.repository` and `x.service` classes.

6. Create and extend `x.service.impl` classes implementing the ext's `x.service`. Add corresponding super call in constructor of all such classes. 
Add annotation `@Service("<ServiceName>")` and `@Primary` annotation to the classes. 

7. Create and extend `x.web.rest` classes.  Add the corresponding super call in constructor of all such classes. 
Add annotation `@RestController("<ResourceName>")` to the class. 

8. If you want both base apis and ext apis to be available, use a different resource mapping such as`@RequestMapping("/api/rest")` in the ext resources.
If you want to ignore the base apis, remove `@RestController` annotation from the base packages.

9. Modify all imports for `repository`, `service`, `impl` and `web.rest` in ext package to import from ext and not from base classes.

# Automating The Entire Pipeline
You may use [script.py](https://github.com/uniquetrij/jhipster-ext/edit/master/script.py) to automate the entire process described above. To do this you need to run the script from the project root, i.e in the folder that contains the `src` folder. Make sure your `x` folder name do not conflict with an existing folder in the project root. 


