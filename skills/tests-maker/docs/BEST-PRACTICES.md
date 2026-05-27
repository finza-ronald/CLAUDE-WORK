# Boas práticas — criação de testes com pytest

Detalhamento das regras referenciadas em [../SKILL.md](../SKILL.md). Cada seção descreve a regra, o motivo e — quando útil — exemplo curto.

---

## 1. Estrutura e localização

- Criar testes na pasta `tests/` de cada app.
- Antes de criar um arquivo novo, localizar o arquivo de teste existente que mais combina com o assunto e adicionar ali.
- Verificar testes próximos para reaproveitar nomenclaturas e estilo.

---

## 2. Ferramentas e bibliotecas

- **pytest** como runner.
- **model_bakery** para criação de dados no banco.
- Usar funcionalidades nativas do framework em uso (Django, FastAPI, Flask, Django Ninja, etc.) em vez de reescrever utilitários.
- Antes de criar uma helper, conferir libs disponíveis no `pyproject.toml`.

---

## 3. Fixtures

- Procurar fixtures úteis nos diversos `conftest.py` do projeto antes de criar dados manualmente.
- Reusar fixtures e factories existentes mesmo quando os dados diferem um pouco: **alterar o retorno da fixture/factory dentro do teste**, sempre com um comentário curto respondendo *"por que essa alteração?"*.
- Não duplicar fixtures só porque um campo é diferente.

---

## 4. Docstrings

- Cada teste tem uma docstring curta, descrevendo o que ele testa (resumo, sem detalhes técnicos).
- Ao criar um arquivo de teste novo, adicionar uma docstring no topo do arquivo explicando:
  - o que aquele arquivo testa;
  - quais são os cenários principais cobertos.

---

## 5. Comentários — quando inserir

Inserir comentários **apenas** nos seguintes casos:

- Para esclarecer o que é esperado de um trecho.
- Para esclarecer o que é esperado para uma variável.
- Para descrever uma regra de negócio sobre uma modificação no dado do banco. Ex.: `# false porque indica que o pagamento deve ser recusado`.

### Evitar comentários

- Comentários óbvios.
- Comentar `if`s descritivos.
- Comentar funções com nome bem descrito.
- Comentar variáveis com nome óbvio.

---

## 6. Mocks

- Preferir **testes funcionais** (com integração leve) à mockagem agressiva.
- Evitar mocks genéricos.
- Sempre que possível, usar `spec=` apontando para a classe que origina o objeto, ex.: `Mock(spec=ServicoCobranca)`. Isso garante que apenas atributos/métodos reais sejam acessíveis no mock.

---

## 7. Testes de API — asserts e `expected_*`

- Em testes que verificam retorno de APIs, criar uma variável `expected_return` ou `expected_<algo>` com nome descritivo e comparar contra ela.
- Isso melhora legibilidade e torna falhas mais óbvias.

Exemplo:

```python
expected_payload = {"status": "approved", "amount": 100}
assert response.json() == expected_payload
```

---

## 8. Sugestões de cenários

Após implementar o teste principal, sugerir ao usuário outros cenários relacionados:

- Caminho infeliz (input inválido, dado ausente, erro do downstream).
- Permissões e autorização.
- Estados intermediários ou de transição.
- Idempotência (quando aplicável).
- Concorrência/duplicidade.

---

## 9. Recursos do framework

Usar recursos nativos do framework em uso:

- **Django**: `Client`, `RequestFactory`, `assertNumQueries`, `override_settings`, `freezegun`/`time_machine` se disponível.
- **FastAPI**: `TestClient`, dependency overrides.
- **Flask**: `test_client`, app contexts.
- **Django Ninja**: client específico do Ninja quando aplicável.

---

## 10. Arrange / Action / Assert

### Arrange

- Criar **o mínimo de dados necessários** para o teste — nada de "popular o banco por garantia".

### Action

- Quando a ação não for clara, adicionar um comentário curto descrevendo o que se espera dela.

### Assert

- Preferir **asserts progressivos**, do mais externo ao mais específico. Exemplos de ordem:

  - **API**: sucesso no retorno → existência do dado → o que era pra ser testado.
  - **Banco**: dados modificados no banco → número de retornos correto → dados esperados corretos → propriedade alterada nos dados.

- Asserts progressivos tornam a falha mais informativa: você sabe **em que etapa** o teste quebrou.

---

## 11. Anti-padrões a evitar

- Comentários inúteis ou óbvios.
- Uso de `getattr`/`hasattr` para "verificar se a propriedade existe" — se há dúvida, o teste/código está mal modelado.
- Variáveis declaradas e não utilizadas.
- Recriar fixtures ou factories existentes apenas porque um dado é diferente.
- Funções auxiliares "criar dado no banco" — manter a inserção dentro do próprio teste.
- Mocks genéricos sem `spec=`.

---

## 12. Inserção de dados no banco

- Preferir **`model_bakery`** para criar instâncias.
- Quando o dado inserido é importante para o teste e **não é salvo em variável**, deixar um comentário curto destacando a importância. Ex.:

```python
# cobrança em status "pending" — necessária para o filtro do endpoint
baker.make("cobrancas.Cobranca", status="pending")
```

---

## 13. Helpers e funções auxiliares

- Evitar criar funções auxiliares na maioria dos casos.
- Em especial, evitar funções "cria dado no banco" — toda manipulação fica dentro do próprio teste.
- Helpers só fazem sentido quando há **muita** repetição não-trivial e não há alternativa via fixture.

---

## 14. Reuso de fixtures e factories

- Não recriar fixtures/factories existentes quando um campo precisa ser diferente.
- Em vez disso, alterar o retorno da fixture/factory dentro do teste, sempre com comentário do "porquê" da alteração.

---

## 15. Preferir funcionalidades existentes

- Usar funções, classes e métodos fornecidos por:
  - Django / Django Ninja / FastAPI / Flask (conforme o framework do projeto).
  - pytest e seus plugins.
  - Outras libs já presentes no `pyproject.toml`.
- Não recriar utilitários que já existem.

---

## 16. Timezone (Django)

- Salvar dados com timezone para evitar warnings do Django.
- Usar `django.utils.timezone.now()` em vez de `datetime.now()`.

---

## 17. Nomenclaturas e consistência

- Antes de nomear um teste, verificar testes próximos para seguir nomenclatura existente.
- Manter consistência com o estilo do arquivo/app.

---

## 18. Não sobrescrever classes e funções existentes

- Não sobrescrever classes e funções existentes dentro do teste.
- Para alterar comportamento temporariamente, usar:
  - **gerenciadores de contexto** (`with override_settings(...)`, `with patch(...)`, `with freeze_time(...)`);
  - **mocks** apropriados (`Mock(spec=...)`).

---

## 19. Formato dos testes

- Testes em formato de **função** (`def test_alguma_coisa(...)`), não em classes.
- Classes de teste só se houver uma razão clara que não seja resolvida por fixtures/parametrize.
