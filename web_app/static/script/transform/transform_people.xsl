<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dssp="http://purl.org/dssp/"
    xmlns:owl="http://www.w3.org/2002/07/owl#" xmlns:pro="http://purl.org/spar/pro" xmlns:proles="http://www.essepuntato.it/2013/10/politicalroles"
    xmlns:prov="http://www.w3.org/ns/prov#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:tei="http://www.tei-c.org/ns/1.0" version="2.0" xmlns:ti="http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#" xmlns:tvc="http://www.essepuntato.it/2012/04/tvc/">
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:param name="BASE_URI"><xsl:value-of select="//tei:TEI/@xml:base"/></xsl:param>
    <xsl:template match="/">
        <rdf:RDF xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dssp="http://purl.org/dssp/" xmlns:owl="http://www.w3.org/2002/07/owl#"
            xmlns:pro="http://purl.org/spar/pro" xmlns:proles="http://www.essepuntato.it/2013/10/politicalroles"
            xmlns:prov="http://www.w3.org/ns/prov#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:tei="http://www.tei-c.org/ns/1.0"
            xmlns:ti="http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#"
            xmlns:tvc="http://www.essepuntato.it/2012/04/tvc/">
            <xsl:apply-templates select="//tei:teiHeader//tei:person"/>
        </rdf:RDF>
    </xsl:template>
    <xsl:template name="cert">
        <xsl:if test=".[@cert]">
            <!-- do something -->
        </xsl:if>
    </xsl:template>
    <xsl:template name="resp">
        <xsl:if test=".[@resp]">
           <!-- do something --> 
        </xsl:if>
    </xsl:template>
    <xsl:template name="relation-desc">
        <rdf:Description rdf:about="{concat($BASE_URI, '/relation/', @xml:id)}">
            <rdf:type>
                <xsl:attribute name="rdf:resource">
                    <xsl:choose>
                        <xsl:when test="parent::tei:listRelation/@type">
                            <xsl:value-of select="concat($BASE_URI, '/relation-type/', parent::tei:listRelation/@type)"/>
                        </xsl:when>
                        <xsl:when test="@type">
                            <xsl:value-of select="concat($BASE_URI, '/relation-type/', @type)"/>
                        </xsl:when>
                        <xsl:otherwise>http://purl.org/vocab/bio/0.1/Relationship</xsl:otherwise>
                    </xsl:choose>
                </xsl:attribute>
            </rdf:type>
        </rdf:Description>
    </xsl:template>
    <xsl:key name="persNameByRef" match="//tei:text//tei:persName[@ref]" use="@ref"/>
    <xsl:key name="relationByActiveParticipant" match="//tei:teiHeader//tei:listPerson//tei:relation" use="tokenize(@active, '\s')"/>
    <xsl:key name="relationByPassiveParticipant" match="//tei:teiHeader//tei:listPerson//tei:relation" use="tokenize(@passive, '\s')"/>
    <xsl:key name="relationByMutualParticipant" match="//tei:teiHeader//tei:listPerson//tei:relation" use="tokenize(@mutual, '\s')"/>
    <xsl:template match="tei:person">
        <xsl:variable name="person-id">
            <xsl:value-of select="@xml:id"/>
        </xsl:variable>
        <rdf:Description rdf:about="{concat($BASE_URI, '/person/', $person-id)}">
            <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
            <xsl:for-each select="tokenize(@sameAs, '\s')">
                <owl:sameAs rdf:resource="{.}"/>
            </xsl:for-each>
            <rdfs:label>
                <xsl:if test="tei:persName/@xml:lang">
                    <xsl:attribute name="xml:lang">
                        <xsl:value-of select="tei:persName/@xml:lang"/>
                    </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="tei:persName"/>
            </rdfs:label>
            <xsl:for-each select="key('persNameByRef', concat('#', string($person-id)))">
                <dcterms:isReferencedBy>
                    <xsl:attribute name="rdf:resource">
                        <xsl:value-of select="$BASE_URI"/>
                        <xsl:choose>
                            <xsl:when test="ancestor::tei:p[1]">
                                <xsl:value-of select="concat('/text/', ancestor::tei:p[1]/@xml:id)"/>
                            </xsl:when>
                            <xsl:when test="ancestor::tei:l[1]">
                                <xsl:value-of select="concat('/text/', ancestor::tei:l[1]/@xml:id)"/>
                            </xsl:when>
                            <xsl:when test="ancestor::tei:div[1]">
                                <xsl:value-of select="concat('/text/', ancestor::tei:div[1]/@xml:id)"/>
                            </xsl:when>
                        </xsl:choose>
                    </xsl:attribute>
                </dcterms:isReferencedBy>
            </xsl:for-each>
            <xsl:if test="parent::tei:listPerson/@type">
                <dcterms:description>
                    <xsl:value-of select="translate(parent::tei:listPerson/@type, '-', ' ')"/>
                </dcterms:description>
            </xsl:if>
            <xsl:for-each
                select="key('relationByActiveParticipant', concat('#', string($person-id))) | key('relationByPassiveParticipant', concat('#', string(@xml:id))) | key('relationByMutualParticipant', concat('#', string(@xml:id)))">
                <pro:holdsRoleInTime rdf:resource="{concat($BASE_URI, '/rit/', $person-id, '-in-', @xml:id)}"/>
            </xsl:for-each>
            <xsl:for-each select="tei:event">
                <pro:holdsRoleInTime rdf:resource="{concat($BASE_URI, '/rit/', $person-id, '-at-', @xml:id)}"/>
            </xsl:for-each>
            <xsl:call-template name="cert"/>
            <xsl:call-template name="resp"/>
        </rdf:Description>
        <xsl:for-each select="key('relationByActiveParticipant', concat('#', string($person-id)))">
            <rdf:Description rdf:about="{concat($BASE_URI, '/rit/', $person-id, '-in-', @xml:id)}">
                <rdf:type rdf:resource="http://purl.org/spar/pro/RoleInTime"/>
                <pro:withRole rdf:resource="{concat($BASE_URI, '/role/', tokenize(@name, '-')[1])}"/>
                <pro:relatesToEntity rdf:resource="{concat($BASE_URI, '/relation/', @xml:id)}"/>
            </rdf:Description>
            <xsl:call-template name="relation-desc"/>
        </xsl:for-each>
        <xsl:for-each select="key('relationByPassiveParticipant', concat('#', string(@xml:id)))">
            <rdf:Description rdf:about="{concat($BASE_URI, '/rit/', $person-id, '-in-', @xml:id)}">
                <rdf:type rdf:resource="http://purl.org/spar/pro/RoleInTime"/>
                <pro:withRole rdf:resource="{concat($BASE_URI, '/role/', tokenize(@name, '-')[2])}"/>
                <pro:relatesToEntity rdf:resource="{concat($BASE_URI, '/relation/', @xml:id)}"/>
            </rdf:Description>
            <xsl:call-template name="relation-desc"/>
        </xsl:for-each>
        <xsl:for-each select="key('relationByMutualParticipant', concat('#', string(@xml:id)))">
            <rdf:Description rdf:about="{concat($BASE_URI, '/rit/', $person-id, '-in-', @xml:id)}">
                <rdf:type rdf:resource="http://purl.org/spar/pro/RoleInTime"/>
                <pro:withRole rdf:resource="{concat($BASE_URI, '/role/', @name)}"/>
                <pro:relatesToEntity rdf:resource="{concat($BASE_URI, '/relation/', @xml:id)}"/>
            </rdf:Description>
            <xsl:call-template name="relation-desc"/>
        </xsl:for-each>
        <xsl:for-each select="tei:event">
            <rdf:Description rdf:about="{concat($BASE_URI, '/rit/', $person-id, '-at-', @xml:id)}">
                <rdf:type rdf:resource="http://purl.org/spar/pro/RoleInTime"/>
                <pro:withRole>
                    <xsl:attribute name="rdf:resource">
                        <xsl:choose>
                            <xsl:when test="tei:desc/tei:persName[@ref=concat('#', $person-id)]">
                                <xsl:value-of
                                    select="concat('http://purl.org/vocab/bio/0.1/', tei:desc/tei:persName[@ref=concat('#', $person-id)]/@role)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>http://purl.org/vocab/bio/0.1/principal</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </pro:withRole>
                <xsl:if test="@when|@from|@to">
                    <tvc:atTime rdf:resource="{concat($BASE_URI, '/tvc/', @xml:id, '-time')}"/>
                </xsl:if>
                <pro:relatesToEntity rdf:resource="{concat($BASE_URI, '/event/', @xml:id)}"/>
                <xsl:if test="tei:desc/tei:placeName">
                    <proles:relatesToPlace rdf:resource="{tei:desc/tei:placeName/@ref}"/>
                </xsl:if>
            </rdf:Description>
            <xsl:if test="@when|@from|@to">
                <rdf:Description rdf:about="{concat($BASE_URI, '/tvc/', @xml:id, '-time')}">
                    <rdf:type rdf:resource="http://www.ontologydesignpatterns.org/cp/owl/timeinterval.owl#TimeInterval"/>
                    <xsl:choose>
                        <xsl:when test="@when">
                            <ti:hasIntervalStartDate>"<xsl:value-of select="@when"></xsl:value-of>"^^xsd:date</ti:hasIntervalStartDate>
                            <ti:hasIntervalEndDate>"<xsl:value-of select="@when"></xsl:value-of>"^^xsd:date</ti:hasIntervalEndDate> 
                        </xsl:when>
                        <xsl:otherwise>
                            <ti:hasIntervalStartDate>"<xsl:value-of select="@from"></xsl:value-of>"^^xsd:date</ti:hasIntervalStartDate>
                            <ti:hasIntervalEndDate>"<xsl:value-of select="@to"></xsl:value-of>"^^xsd:date</ti:hasIntervalEndDate>
                        </xsl:otherwise>
                    </xsl:choose>
                </rdf:Description>
            </xsl:if>
            <rdf:Description rdf:about="{concat($BASE_URI, '/event/', @xml:id)}">
                <rdf:type>
                    <xsl:attribute name="rdf:resource">
                        <xsl:choose>
                            <xsl:when test="@type">
                                <xsl:value-of select="concat('http://purl.org/vocab/bio/0.1/', @type)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>http://purl.org/vocab/bio/0.1/Event</xsl:text>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:attribute>
                </rdf:type>
                <rdf:label>
                    <xsl:value-of select="tei:label"/>
                </rdf:label>
                <xsl:if test="tei:bibl">
                    <prov:hasPrimarySource rdf:resource="{concat($BASE_URI, '/source/', tei:bibl/@xml:id)}"/>
                </xsl:if>
            </rdf:Description>
            <xsl:if test="tei:bibl">
                <rdf:Description rdf:about="{concat($BASE_URI, '/source/', tei:bibl/@xml:id)}">
                    <rdf:type rdf:resource="http://www.w3.org/ns/prov#PrimarySource"/>
                    <xsl:if test="tei:bibl/tei:author">
                        <dcterms:creator rdf:resource="{concat($BASE_URI, '/person/', translate(tei:bibl/tei:author/@ref, '#', ''))}"/>
                    </xsl:if>
                    <xsl:if test="tei:bibl/tei:title">
                        <dcterms:title>"<xsl:value-of select="tei:bibl/tei:title"></xsl:value-of></dcterms:title>
                    </xsl:if>
                    <xsl:if test="tei:bibl/@sameAs">
                        <owl:sameAs rdf:resource="{tei:bibl/@sameAs}"/>
                    </xsl:if>
                </rdf:Description>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>